import urllib3


def get_host(url: str) -> str:
    return urllib3.util.parse_url(url).hostname


def get_path_format(path: str, dirname: str) -> str:
    if dirname == '':
        return ''
    else:
        if path == '':
            return dirname
        else:
            return path + '/' + dirname


def get_dirname_path_parts(dirname_param: str, path_param: str) -> (str, str):
    route = '/db?path={}&dirname={}'

    if dirname_param == '':
        path_parts = []
        dirname = 'root'
    else:
        path_parts = [{
            'name': 'root',
            'href': route.format('', ''),
        }]
        dirname = dirname_param

        # if path no empty, parse it
        if path_param != '':

            path_list = path_param.split('.')

            for i in range(len(path_list)):
                pointed_path = "/".join(path_list[:i])
                name = path_list[i]

                path_parts.append({
                    'name': name,
                    'href': route.format(pointed_path, name)
                })

    return dirname, path_parts


def get_dir_content(dirs: list, path_param: str, dirname_param: str):
    route_dir = '/db?path={}&dirname={}'
    route_entry = '/db/entry?path={}&dirname={}&entry={}'

    dir_content = []

    for d in dirs:
        name = d['name']

        if d['type'] == 'entry':
            href = route_entry.format(
                path_param, dirname_param, name
            )

        else:
            if dirname_param == '':
                pointed_path = ''
            elif path_param == '':
                pointed_path = dirname_param
            else:
                pointed_path = f"{path_param}.{dirname_param}"

            href = route_dir.format(pointed_path, name)

        di = d
        di['href'] = href
        dir_content.append(di)

    return dir_content
