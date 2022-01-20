import climmob.plugins as plugins
import climmob.plugins.utilities as u
from packagesWithTechnologiesExtension.celerytasks import createQRWithTechnologies
import sys
import os
from climmob.products.climmob_products import (
    createProductDirectory,
    registerProductInstance,
)


class packagesWithTechnologiesExtension(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfig)
    plugins.implements(plugins.ITranslation)
    plugins.implements(plugins.IpackagesWithTechnologiesExtension)

    def update_config(self, config):
        # We add here the templates of the plugin to the config
        u.addTemplatesDirectory(config, "templates")

    def get_translation_directory(self):
        module = sys.modules["packagesWithTechnologiesExtension"]
        return os.path.join(os.path.dirname(module.__file__), "locale")

    def get_translation_domain(self):
        return "packagesWithTechnologiesExtension"

    def create_qr_packages_with_technologies(
        self, request, locale, userOwner, projectId, projectCod, options, packages
    ):
        path = createProductDirectory(
            request, userOwner, projectCod, "qrpackagewithtechnologies"
        )

        task = createQRWithTechnologies.apply_async(
            (locale, path, projectCod, packages), queue="ClimMob"
        )

        registerProductInstance(
            projectId,
            "qrpackagewithtechnologies",
            "packages_with_technologies_" + projectCod + ".pdf",
            "application/pdf",
            "create_packages_with_technologies",
            task.id,
            request,
        )
