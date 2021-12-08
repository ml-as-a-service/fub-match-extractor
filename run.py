import functions as fx
# -----------------------------------------------------------------------------
# Inicializamos la estructura de carpetas
fx.init()

# -----------------------------------------------------------------------------
# Bajamos la pagina en tmp/download/MapaEstHid.aspx utilizando requests
url = "https://hosted.dcd.shared.geniussports.com/embednf/FUBB/es/competition/30436/match/2009972/playbyplay?&iurl=http%3A%2F%2Fwww.fubb.org.uy%2F%3Fp%3D9&_cc=1&_lc=1&_nv=1&_mf=1"
file_path = fx.download(url)

# -----------------------------------------------------------------------------
# Obtenemos las actions en una lista utilizando BeautifulSoup
matchAction = fx.getMatchAction(file_path)
# print(matchAction)
# -----------------------------------------------------------------------------
# Exportamos las actions a CSV utilizando pandas
file_name_csv = fx.dir_data+"MatchAction.csv"
fx.exportToCsv(matchAction, file_name_csv)
