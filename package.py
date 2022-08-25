name = "otio_cdl_adapter"
version = "0.7.0"
authors = ['John Mission']
help = 'https://github.com/josh-mission/otio-cdl-adapter'
description = "OpenTimelineIO CDL Adapter"
plugin_for = ['OpenTimelineIO']
requires = [
  'OpenTimelineIO-0.12+',
]

@early()
def uuid():
    import uuid
    return str(uuid.uuid5(uuid.NAMESPACE_DNS, name))

build_command = """
rsync -avP {root}/$REZ_BUILD_PROJECT_NAME $REZ_BUILD_INSTALL_PATH
"""

def commands():
  env.OTIO_PLUGIN_MANIFEST_PATH.append('{root}/{this.name}/plugin_manifest.json')

