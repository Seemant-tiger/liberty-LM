config = {'search_dict': {}}

def init(sources):
    if 'GP' in sources:
        from scraping.googleplaces import main as gp_main
        config['search_dict']['GP'] = gp_main

    if 'CH' in sources:
        from scraping.companyhouse import main as ch_main
        config['search_dict']['CH'] = ch_main

    if 'ZI' in sources:
        from scraping.zoominfo import main as zi_main
        config['search_dict']['ZI'] = zi_main

    if 'FS' in sources:
        from scraping.foursquare import main as fs_main
        config['search_dict']['FS'] = fs_main