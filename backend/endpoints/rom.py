import os
from datetime import datetime
from shutil import rmtree
from stat import S_IFREG
from typing import Annotated
from urllib.parse import quote

from config import (
    DISABLE_DOWNLOAD_ENDPOINT_AUTH,
    LIBRARY_BASE_PATH,
    RESOURCES_BASE_PATH,
)
from decorators.auth import protected_route
from endpoints.responses import MessageResponse
from endpoints.responses.rom import (
    AddRomsResponse,
    CustomStreamingResponse,
    DetailedRomSchema,
    RomPropsSchema,
    RomSchema,
)
from exceptions.fs_exceptions import RomAlreadyExistsException
from fastapi import APIRouter, File, HTTPException, Query, Request, UploadFile, status
from fastapi.responses import FileResponse
from handler.database import db_platform_handler, db_rom_handler
from handler.filesystem import fs_resource_handler, fs_rom_handler
from handler.metadata import meta_igdb_handler, meta_moby_handler
from logger.logger import log
from stream_zip import ZIP_AUTO, stream_zip  # type: ignore[import]

router = APIRouter()


@protected_route(router.post, "/roms", ["roms.write"])
def add_roms(
    request: Request,
    platform_id: int,
    roms: list[UploadFile] = File(...),  # noqa: B008
) -> AddRomsResponse:
    """Upload roms endpoint (one or more at the same time)

    Args:
        request (Request): Fastapi Request object
        platform_slug (str): Slug of the platform where to upload the roms
        roms (list[UploadFile], optional): List of files to upload. Defaults to File(...).

    Raises:
        HTTPException: No files were uploaded

    Returns:
        AddRomsResponse: Standard message response
    """

    platform_fs_slug = db_platform_handler.get_platforms(platform_id).fs_slug
    log.info(f"Uploading roms to {platform_fs_slug}")
    if roms is None:
        log.error("No roms were uploaded")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="No roms were uploaded",
        )

    roms_path = fs_rom_handler.build_upload_file_path(platform_fs_slug)

    uploaded_roms = []
    skipped_roms = []

    for rom in roms:
        if fs_rom_handler.file_exists(roms_path, rom.filename):
            log.warning(f" - Skipping {rom.filename} since the file already exists")
            skipped_roms.append(rom.filename)
            continue

        log.info(f" - Uploading {rom.filename}")
        file_location = f"{roms_path}/{rom.filename}"

        with open(file_location, "wb+") as f:
            while True:
                chunk = rom.file.read(1024)
                if not chunk:
                    break
                f.write(chunk)

        uploaded_roms.append(rom.filename)

    return {
        "uploaded_roms": uploaded_roms,
        "skipped_roms": skipped_roms,
    }


@protected_route(router.get, "/roms", ["roms.read"])
def get_roms(
    request: Request,
    platform_id: int | None = None,
    search_term: str = "",
    limit: int | None = None,
    order_by: str = "name",
    order_dir: str = "asc",
) -> list[RomSchema]:
    """Get roms endpoint

    Args:
        request (Request): Fastapi Request object
        id (int, optional): Rom internal id

    Returns:
        list[RomSchema]: List of roms stored in the database
    """

    with db_rom_handler.session.begin() as session:
        return session.scalars(
            db_rom_handler.get_roms(
                platform_id=platform_id,
                search_term=search_term.lower(),
                order_by=order_by.lower(),
                order_dir=order_dir.lower(),
            ).limit(limit)
        ).all()


@protected_route(
    router.get,
    "/roms/{id}",
    [] if DISABLE_DOWNLOAD_ENDPOINT_AUTH else ["roms.read"],
)
def get_rom(request: Request, id: int) -> DetailedRomSchema:
    """Get rom endpoint

    Args:
        request (Request): Fastapi Request object
        id (int): Rom internal id

    Returns:
        DetailedRomSchema: Rom stored in the database
    """
    return DetailedRomSchema.from_orm_with_request(db_rom_handler.get_roms(id), request)


@protected_route(
    router.head,
    "/roms/{id}/content/{file_name}",
    [] if DISABLE_DOWNLOAD_ENDPOINT_AUTH else ["roms.read"],
)
def head_rom_content(request: Request, id: int, file_name: str):
    """Head rom content endpoint

    Args:
        request (Request): Fastapi Request object
        id (int): Rom internal id
        file_name (str): Required due to a bug in emulatorjs

    Returns:
        FileResponse: Returns the response with headers
    """

    rom = db_rom_handler.get_roms(id)
    rom_path = f"{LIBRARY_BASE_PATH}/{rom.full_path}"

    return FileResponse(
        path=rom_path if not rom.multi else f"{rom_path}/{rom.files[0]}",
        filename=file_name,
        headers={
            "Content-Disposition": f'attachment; filename="{quote(rom.name)}.zip"',
            "Content-Type": "application/zip",
            "Content-Length": str(rom.file_size_bytes),
        },
    )


@protected_route(router.get, "/roms/{id}/content/{file_name}", ["roms.read"])
def get_rom_content(
    request: Request,
    id: int,
    file_name: str,
    files: Annotated[list[str] | None, Query()] = None,
):
    """Download rom endpoint (one single file or multiple zipped files for multi-part roms)

    Args:
        request (Request): Fastapi Request object
        id (int): Rom internal id
        files (Annotated[list[str]  |  None, Query, optional): List of files to download for multi-part roms. Defaults to None.

    Returns:
        FileResponse: Returns one file for single file roms

    Yields:
        CustomStreamingResponse: Streams a file for multi-part roms
    """

    rom = db_rom_handler.get_roms(id)
    rom_path = f"{LIBRARY_BASE_PATH}/{rom.full_path}"
    files_to_download = files or rom.files

    if not rom.multi:
        return FileResponse(path=rom_path, filename=rom.file_name)

    if len(files_to_download) == 1:
        return FileResponse(
            path=f"{rom_path}/{files_to_download[0]}", filename=files_to_download[0]
        )

    # Builds a generator of tuples for each member file
    def local_files():
        def contents(f):
            try:
                with open(f"{rom_path}/{f}", "rb") as f:
                    while chunk := f.read(65536):
                        yield chunk
            except FileNotFoundError:
                log.error(f"File {rom_path}/{f} not found!")
                raise

        m3u_file = [
            str.encode(f"{files_to_download[i]}\n")
            for i in range(len(files_to_download))
        ]
        return [
            (
                f,
                datetime.now(),
                S_IFREG | 0o600,
                ZIP_AUTO(os.path.getsize(f"{rom_path}/{f}")),
                contents(f),
            )
            for f in files_to_download
        ] + [
            (
                f"{file_name}.m3u",
                datetime.now(),
                S_IFREG | 0o600,
                ZIP_AUTO(sum([len(f) for f in m3u_file])),
                m3u_file,
            )
        ]

    zipped_chunks = stream_zip(local_files())

    # Streams the zip file to the client
    return CustomStreamingResponse(
        zipped_chunks,
        media_type="application/zip",
        headers={
            "Content-Disposition": f'attachment; filename="{quote(file_name)}.zip"'
        },
        emit_body={"id": rom.id},
    )


@protected_route(router.put, "/roms/{id}", ["roms.write"])
async def update_rom(
    request: Request,
    id: int,
    rename_as_source: bool = False,
    remove_cover: bool = False,
    artwork: UploadFile | None = None,
) -> DetailedRomSchema:
    """Update rom endpoint

    Args:
        request (Request): Fastapi Request object
        id (Rom): Rom internal id
        rename_as_source (bool, optional): Flag to rename rom file as matched IGDB game. Defaults to False.
        artwork (UploadFile, optional): Custom artork to set as cover. Defaults to File(None).

    Raises:
        HTTPException: If a rom already have that name when enabling the rename_as_source flag

    Returns:
        DetailedRomSchema: Rom stored in the database
    """

    data = await request.form()

    db_rom = db_rom_handler.get_roms(id)

    cleaned_data = {}
    cleaned_data["igdb_id"] = data.get("igdb_id", None)
    cleaned_data["moby_id"] = data.get("moby_id", None)

    if cleaned_data["moby_id"]:
        moby_rom = meta_moby_handler.get_rom_by_id(cleaned_data["moby_id"])
        cleaned_data.update(moby_rom)
    else:
        cleaned_data.update({"moby_metadata": {}})

    if cleaned_data["igdb_id"]:
        igdb_rom = meta_igdb_handler.get_rom_by_id(cleaned_data["igdb_id"])
        cleaned_data.update(igdb_rom)
    else:
        cleaned_data.update({"igdb_metadata": {}})

    cleaned_data["name"] = data.get("name", db_rom.name)
    cleaned_data["summary"] = data.get("summary", db_rom.summary)

    fs_safe_file_name = (
        data.get("file_name", db_rom.file_name).strip().replace("/", "-")
    )
    fs_safe_name = cleaned_data["name"].strip().replace("/", "-")

    if rename_as_source:
        fs_safe_file_name = db_rom.file_name.replace(
            db_rom.file_name_no_tags or db_rom.file_name_no_ext, fs_safe_name
        )

    try:
        if db_rom.file_name != fs_safe_file_name:
            fs_rom_handler.rename_file(
                old_name=db_rom.file_name,
                new_name=fs_safe_file_name,
                file_path=db_rom.file_path,
            )
    except RomAlreadyExistsException as exc:
        log.error(str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(exc)
        ) from exc

    cleaned_data["file_name"] = fs_safe_file_name
    cleaned_data["file_name_no_tags"] = fs_rom_handler.get_file_name_with_no_tags(
        fs_safe_file_name
    )
    cleaned_data["file_name_no_ext"] = fs_rom_handler.get_file_name_with_no_extension(
        fs_safe_file_name
    )

    if remove_cover:
        cleaned_data.update(fs_resource_handler.remove_cover(rom=db_rom))
        cleaned_data.update({"url_cover": ""})
    else:
        if artwork is not None:
            file_ext = artwork.filename.split(".")[-1]
            (
                path_cover_l,
                path_cover_s,
                artwork_path,
            ) = fs_resource_handler.build_artwork_path(db_rom, file_ext)

            cleaned_data["path_cover_l"] = path_cover_l
            cleaned_data["path_cover_s"] = path_cover_s

            artwork_file = artwork.file.read()
            file_location_s = f"{artwork_path}/small.{file_ext}"
            with open(file_location_s, "wb+") as artwork_s:
                artwork_s.write(artwork_file)
                fs_resource_handler.resize_cover_to_small(file_location_s)

            file_location_l = f"{artwork_path}/big.{file_ext}"
            with open(file_location_l, "wb+") as artwork_l:
                artwork_l.write(artwork_file)
        else:
            cleaned_data["url_cover"] = data.get("url_cover", db_rom.url_cover)
            path_cover_s, path_cover_l = fs_resource_handler.get_rom_cover(
                overwrite=True,
                rom=db_rom,
                url_cover=cleaned_data.get("url_cover", ""),
            )
            cleaned_data.update(
                {"path_cover_s": path_cover_s, "path_cover_l": path_cover_l}
            )

    if (
        cleaned_data["igdb_id"] != db_rom.igdb_id
        or cleaned_data["moby_id"] != db_rom.moby_id
    ):
        path_screenshots = fs_resource_handler.get_rom_screenshots(
            rom=db_rom,
            url_screenshots=cleaned_data.get("url_screenshots", []),
        )
        cleaned_data.update({"path_screenshots": path_screenshots})

    db_rom_handler.update_rom(id, cleaned_data)
    updated_rom = db_rom_handler.get_roms(id)

    # db_rom_handler.set_main_sibling(updated_rom)

    return DetailedRomSchema.from_orm_with_request(updated_rom, request)


@protected_route(router.post, "/roms/delete", ["roms.write"])
async def delete_roms(
    request: Request,
) -> MessageResponse:
    """Delete roms endpoint

    Args:
        request (Request): Fastapi Request object.
            {
                "roms": List of rom's ids to delete
            }
        delete_from_fs (bool, optional): Flag to delete rom from filesystem. Defaults to False.

    Returns:
        MessageResponse: Standard message response
    """

    data: dict = await request.json()
    roms_ids: list = data["roms"]
    delete_from_fs: list = data["delete_from_fs"]

    for id in roms_ids:
        rom = db_rom_handler.get_roms(id)
        if not rom:
            error = f"Rom with id {id} not found"
            log.error(error)
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)

        log.info(f"Deleting {rom.file_name} from database")
        db_rom_handler.delete_rom(id)

        try:
            rmtree(f"{RESOURCES_BASE_PATH}/{rom.fs_resources_path}")
        except FileNotFoundError:
            log.error(f"Couldn't find resources to delete for {rom.name}")

        if id in delete_from_fs:
            log.info(f"Deleting {rom.file_name} from filesystem")
            try:
                fs_rom_handler.remove_file(
                    file_name=rom.file_name, file_path=rom.file_path
                )
            except FileNotFoundError as exc:
                error = f"Rom file {rom.file_name} not found for platform {rom.platform_slug}"
                log.error(error)
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail=error
                ) from exc

    return {"msg": f"{len(roms_ids)} roms deleted successfully!"}


@protected_route(router.put, "/roms/{id}/props", ["rom_props.write"])
async def update_rom_props(request: Request, id: int) -> RomPropsSchema:
    db_rom = db_rom_handler.get_roms(id)
    if not db_rom:
        error = f"Rom with id {id} could not be found"
        log.error(error)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=error)
    db_rom_props = db_rom_handler.get_rom_props(id, request.user.id)
    if not db_rom_props:
        db_rom_props = db_rom_handler.add_rom_props(id, request.user.id)

    data = await request.json()
    db_rom_handler.update_rom_props(
        db_rom_props.id,
        {
            "note_raw_markdown": data.get(
                "note_raw_markdown", db_rom_props.note_raw_markdown
            ),
            "note_is_public": data.get("note_is_public", db_rom_props.note_is_public),
            "is_main_sibling": data.get(
                "is_main_sibling", db_rom_props.is_main_sibling
            ),
        },
    )

    db_rom_props = db_rom_handler.get_rom_props(id, request.user.id)
    if db_rom_props.is_main_sibling:
        db_rom_handler.set_main_sibling(db_rom, db_rom_props.user_id)
    return db_rom_props
