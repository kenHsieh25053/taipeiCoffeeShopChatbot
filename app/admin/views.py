from flask_admin.contrib.sqla import ModelView


class ShopAdmin(ModelView):
    column_searchable_list = ['name', 'address']
    column_filters = ['address', 'open_hour',
                      'close_date', 'style', 'price_level', 'space', 'plug_number']
    can_export = True


class FavoriteAdmin(ModelView):
    can_create = False
    can_edit = False
    can_delete = False
    column_searchable_list = ['shop']
