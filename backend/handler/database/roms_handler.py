import functools

from decorators.database import begin_session
from models.rom import Rom, UserRomProps
from sqlalchemy import and_, delete, func, or_, select, update
from sqlalchemy.orm import Query, Session, selectinload

from .base_handler import DBBaseHandler


def with_assets(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        session = kwargs.get("session")
        if session is None:
            raise ValueError("session is required")

        kwargs["query"] = select(Rom).options(
            selectinload(Rom.saves),
            selectinload(Rom.states),
            selectinload(Rom.screenshots),
            selectinload(Rom.user_rom_props),
        )
        return func(*args, **kwargs)

    return wrapper


class DBRomsHandler(DBBaseHandler):
    def _filter(self, data, platform_id: int | None, search_term: str):
        if platform_id:
            data = data.filter_by(platform_id=platform_id)

        if search_term:
            data = data.filter(
                or_(
                    Rom.file_name.ilike(f"%{search_term}%"),  # type: ignore[attr-defined]
                    Rom.name.ilike(f"%{search_term}%"),  # type: ignore[attr-defined]
                )
            )

        return data

    def _order(self, data, order_by: str, order_dir: str):
        if order_by == "id":
            _column = Rom.id
        else:
            _column = func.lower(Rom.name)

        if order_dir == "desc":
            return data.order_by(_column.desc())
        else:
            return data.order_by(_column.asc())

    @begin_session
    @with_assets
    def add_rom(self, rom: Rom, query: Query = None, session: Session = None) -> Rom:
        rom = session.merge(rom)
        session.flush()

        return session.scalar(query.filter_by(id=rom.id).limit(1))

    @begin_session
    @with_assets
    def get_roms(
        self,
        id: int | None = None,
        platform_id: int | None = None,
        search_term: str = "",
        order_by: str = "name",
        order_dir: str = "asc",
        query: Query = None,
        session: Session = None,
    ) -> list[Rom] | Rom | None:
        return (
            session.scalar(query.filter_by(id=id).limit(1))
            if id
            else self._order(
                self._filter(select(Rom), platform_id, search_term),
                order_by,
                order_dir,
            )
        )

    @begin_session
    @with_assets
    def get_rom_by_filename(
        self,
        platform_id: int,
        file_name: str,
        query: Query = None,
        session: Session = None,
    ) -> Rom | None:
        return session.scalar(
            query.filter_by(platform_id=platform_id, file_name=file_name).limit(1)
        )

    @begin_session
    @with_assets
    def get_rom_by_filename_no_tags(
        self, file_name_no_tags: str, query: Query = None, session: Session = None
    ) -> Rom | None:
        return session.scalar(
            query.filter_by(file_name_no_tags=file_name_no_tags).limit(1)
        )

    @begin_session
    @with_assets
    def get_rom_by_filename_no_ext(
        self, file_name_no_ext: str, query: Query = None, session: Session = None
    ) -> Rom | None:
        return session.scalar(
            query.filter_by(file_name_no_ext=file_name_no_ext).limit(1)
        )

    @begin_session
    def update_rom(self, id: int, data: dict, session: Session = None) -> Rom:
        return session.execute(
            update(Rom)
            .where(Rom.id == id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )

    @begin_session
    def set_main_sibling(self, rom: Rom, user_id: int, session: Session = None) -> None:
        siblings = [rom.id for rom in rom.get_sibling_roms()]
        return session.execute(
            update(UserRomProps)
            .where(
                and_(UserRomProps.rom_id.in_(siblings), UserRomProps.user_id == user_id)
            )
            .values(is_main_sibling=False)
        )

    @begin_session
    def delete_rom(self, id: int, session: Session = None) -> Rom:
        return session.execute(
            delete(Rom)
            .where(Rom.id == id)
            .execution_options(synchronize_session="evaluate")
        )

    @begin_session
    def purge_roms(
        self, platform_id: int, roms: list[str], session: Session = None
    ) -> int:
        return session.execute(
            delete(Rom)
            .where(and_(Rom.platform_id == platform_id, Rom.file_name.not_in(roms)))  # type: ignore[attr-defined]
            .execution_options(synchronize_session="evaluate")
        )

    @begin_session
    def get_rom_props(
        self, rom_id: int, user_id: int, session: Session = None
    ) -> UserRomProps | None:
        return session.scalar(
            select(UserRomProps).filter_by(rom_id=rom_id, user_id=user_id).limit(1)
        )

    @begin_session
    def add_rom_props(
        self, rom_id: int, user_id: int, session: Session = None
    ) -> UserRomProps:
        return session.merge(UserRomProps(rom_id=rom_id, user_id=user_id))

    @begin_session
    def update_rom_props(
        self, id: int, data: dict, session: Session = None
    ) -> UserRomProps:
        return session.execute(
            update(UserRomProps)
            .where(UserRomProps.id == id)
            .values(**data)
            .execution_options(synchronize_session="evaluate")
        )
