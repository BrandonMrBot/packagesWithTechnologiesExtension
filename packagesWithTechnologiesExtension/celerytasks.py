from climmob.config.celery_app import celeryApp
from climmob.plugins.utilities import climmobCeleryTask
from jinja2 import Environment, FileSystemLoader
import shutil as sh
import gettext
import qrcode
import base64
import imgkit
import uuid
import bz2
import os


PATH = os.path.dirname(os.path.abspath(__file__))

TEMPLATE_ENVIRONMENT = Environment(
    autoescape=False,
    loader=FileSystemLoader(os.path.join(PATH, "resources", "templates")),
    trim_blocks=False,
)


def render_template(template_filename, context):
    return TEMPLATE_ENVIRONMENT.get_template(template_filename).render(context)


def create_index_html(html, png, qrid, packageid, projectid, projectname, optionsList):

    context = {
        "qrid": qrid,
        "packageid": packageid,
        "projectid": projectid,
        "projectname": projectname,
        "optionsList": optionsList,
    }
    options = {"crop-w": 400, "log-level": "none"}

    with open(html, "w") as f:

        res = render_template("app.jinja2", context)
        f.write(res)

    imgkit.from_url(html, png, options=options)


@celeryApp.task(
    bind=True, base=climmobCeleryTask, soft_time_limit=7200, time_limit=7200
)
def createQRWithTechnologies(self, locale, path, projectid, packages):
    if os.path.exists(path):
        sh.rmtree(path)

    PATH_lo = os.path.dirname(os.path.abspath(__file__))
    this_file_path = PATH_lo + "/locale"

    try:
        es = gettext.translation(
            "packagesWithTechnologiesExtension",
            localedir=this_file_path,
            languages=[locale],
        )
        es.install()
        _ = es.gettext
    except:
        locale = "en"
        es = gettext.translation(
            "packagesWithTechnologiesExtension",
            localedir=this_file_path,
            languages=[locale],
        )
        es.install()
        _ = es.gettext

    os.makedirs(path)
    pathout = os.path.join(path, "outputs")
    os.makedirs(pathout)

    pathfinal = os.path.join(
        path, *["outputs", "packages_with_technologies_" + projectid + ".pdf"]
    )

    path = os.path.join(path, "packages")

    os.makedirs(path)
    os.makedirs(os.path.join(path, "qr"))
    os.makedirs(os.path.join(path, "htmls"))
    os.makedirs(os.path.join(path, "png"))
    os.makedirs(os.path.join(path, "pdf"))

    pathqr = os.path.join(path, "qr")
    pathhtmls = os.path.join(path, "htmls")
    pathpng = os.path.join(path, "png")
    pathpdf = os.path.join(path, "pdf")
    uuidVal = uuid.uuid4()
    pathpdf = os.path.join(pathpdf, str(uuidVal))

    os.mkdir(pathpdf)

    allPNGpaths = ""
    contador = 1
    veces = 0
    for package in packages:

        if self.is_aborted():
            sh.rmtree(path)
            return ""

        qr, optionsList = create_qr(package, projectid, pathqr)

        # HTMLS
        os.system(
            "cp -r '"
            + os.path.join(PATH, "resources", "templates", "css")
            + "' '"
            + pathhtmls
            + "'"
        )
        os.system(
            "cp -r '"
            + os.path.join(PATH, "resources", "templates", "img")
            + "' '"
            + pathhtmls
            + "'"
        )
        html = pathhtmls + "/" + str(package["package_id"]) + ".html"
        png = pathpng + "/" + str(package["package_id"]) + ".png"
        create_index_html(
            html,
            png,
            qr,
            _("Package ") + str(package["package_id"]),
            projectid,
            package["project_name"],
            optionsList,
        )

        allPNGpaths += png + " "

        if contador == 296:
            veces = veces + 1
            os.system(
                "pdfjam "
                + allPNGpaths
                + "  --no-landscape --nup 2x4 --frame true --outfile "
                + pathpdf
                + "/"
                + str(veces)
                + ".pdf"
            )
            os.system(
                "pdfcrop --margin '0 20 0 20' "
                + pathpdf
                + "/"
                + str(veces)
                + ".pdf "
                + pathpdf
                + "/"
                + str(veces)
                + ".pdf"
            )
            allPNGpaths = ""
            contador = 0
        contador = contador + 1

    if allPNGpaths != "":
        veces = veces + 1
        os.system(
            "pdfjam "
            + allPNGpaths
            + "  --no-landscape --nup 2x4 --frame true --outfile "
            + pathpdf
            + "/"
            + str(veces)
            + ".pdf"
        )
        os.system(
            "pdfcrop --margin '0 20 0 20' "
            + pathpdf
            + "/"
            + str(veces)
            + ".pdf "
            + pathpdf
            + "/"
            + str(veces)
            + ".pdf"
        )

    if self.is_aborted():
        sh.rmtree(path)
        return ""

    os.system("pdfjam " + pathpdf + "/*.pdf --no-landscape  --outfile " + pathfinal)

    sh.rmtree(path)

    return ""


def create_qr(package, projectid, pathqr, all=True):
    packageData = ""

    finalData = (
        str(package["user_fullname"])
        + "|"
        + str(package["package_id"])
        + "|"
        + str(package["project_pi"])
        + "|"
        + str(package["project_piemail"])
        + "|"
        + str(package["project_numobs"])
        + "|"
        + str(package["project_numcom"])
        + "|"
    )

    optionsList = []

    for combination in package["combs"]:
        technologies = ""
        options = ""
        optionsStringList = ""

        for tec in combination["technologies"]:
            if options == "":
                technologies += tec["tech_name"]
                options += tec["alias_name"]
                optionsStringList += tec["alias_name"]

            else:
                technologies += "[t]" + tec["tech_name"]
                options += "[o]" + tec["alias_name"]
                optionsStringList += " - " + tec["alias_name"]

        optionsList.append(optionsStringList)

        if packageData == "":
            packageData += chr(64 + combination["comb_order"]) + "[p]" + options
        else:
            packageData += "~" + chr(64 + combination["comb_order"]) + "[p]" + options

    finalData += technologies + "|" + packageData

    # QR
    compressed = bz2.compress(finalData.encode())
    data = (
        str(package["user_name"])
        + "-"
        + str(package["package_id"])
        + "-"
        + projectid
        + "~"
    )
    if all:
        data += str(base64.b64encode(compressed))

    myCode = qrcode.make(data)
    qr = pathqr + "/" + str(package["package_id"]) + ".png"
    myCode.save(qr)

    return qr, optionsList
