from handler.auth_handler.auth_handler import AuthHandler, OAuthHandler
from handler.db_handler.db_platforms_handler import DBPlatformsHandler
from handler.db_handler.db_roms_handler import DBRomsHandler
from handler.fs_handler.fs_assets_handler import FSAssetsHandler
from handler.fs_handler.fs_platforms_handler import FSPlatformsHandler
from handler.fs_handler.fs_resources_handler import FSResourceHandler
from handler.fs_handler.fs_roms_handler import FSRomsHandler
from handler.gh_handler import GHHandler
from handler.igdb_handler import IGDBHandler
from handler.sgdb_handler import SGDBHandler
from handler.socket_handler import SocketHandler

igdbh = IGDBHandler()
sgdbh = SGDBHandler()
ghh = GHHandler()
authh = AuthHandler()
oauthh = OAuthHandler()
socketh = SocketHandler()
dbplatformh = DBPlatformsHandler()
dbromh = DBRomsHandler()
fsplatformh = FSPlatformsHandler()
fsromh = FSRomsHandler()
fsasseth = FSAssetsHandler()
fsresourceh = FSResourceHandler()


from handler.db_handler.db_handler import DBHandler 
dbh = DBHandler()
