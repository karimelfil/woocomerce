from treebeard.mp_tree import MP_Node
from decimal import Decimal
from django.db import models
from decimal import Decimal, ROUND_HALF_UP, ROUND_HALF_DOWN, ROUND_HALF_EVEN, ROUND_UP, ROUND_DOWN, ROUND_CEILING, ROUND_FLOOR

UNIT_OF_MEASURE_OPTIONS = [
    ('length', 'length'),
    ('width', 'width'),
    ('height', 'height'),
    ('weight', 'weight'),
]


def round_value(value):
    return value


def path_and_rename(instance, filename):
    print('fileenamwee', filename)
    upload_to = 'itemimage/'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}{}.{}'.format('item-', instance.sku_code, ext)
    else:
        # set filename as random string
        filename = '{}{}.{}'.format('item-', instance.sku_code, ext)
    # return the whole path to the file
    print('on uploaddd', os.path.join(upload_to, filename))
    return os.path.join(upload_to, filename)



class Activity(models.Model):
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    date_modified = models.DateTimeField(auto_now=True, null=True)
    # created_by = models.ForeignKey(
    #     'authentication.CustomUser',
    #     on_delete=models.CASCADE,
    #     related_name="%(app_label)s_%(class)s_created",
    #     null=True,
    #     blank=True)
    # modified_by = models.ForeignKey(
    #     'authentication.CustomUser',
    #     on_delete=models.CASCADE,
    #     related_name="%(app_label)s_%(class)s_modified",
    #     null=True,
    #     blank=True)
    time_created = models.TimeField(
        auto_now=False,
        auto_now_add=True,
        null=True,
        blank=True)

    class Meta:
        abstract = True
        # #verbose_name_plural = "activity"
        # #db_table  = "activity"




class ItemCategory(MP_Node, Activity):
    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(null=True, blank=True)
    node_order_by = ['path']
    sibling_order_by = ['path']

    class Meta:
        verbose_name = "item_category"
        db_table = "item_category"

    def __str__(self):
        return self.name


class ItemFamily(Activity):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "item_family"
        db_table = "item_family"

    def __str__(self):
        return self.name


class ItemBrand(Activity):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "item_brand"
        db_table = "item_brand"

    def __str__(self):
        return self.name


class Specs(Activity):
    description = models.TextField(null=True, blank=True, unique=True)

    class Meta:
        verbose_name_plural = "item_specification"
        db_table = "item_specification"


class UnitOfMeasurment(Activity):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=50, unique=True, null=True, blank=True)
    type = models.ArrayField(
        models.CharField(max_length=10, choices=UNIT_OF_MEASURE_OPTIONS),
        default=None, blank=True, null=True
    )

    class Meta:
        verbose_name_plural = "unit_of_measurement"
        db_table = "unit_of_measurement"


class Tags(Activity):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "item_tags"
        db_table = "item_tags"


class Package(Activity):
    name = models.CharField(max_length=255)
    weight = models.FloatField(null=True, blank=True)
    length = models.FloatField(null=True, blank=True)
    height = models.FloatField(null=True, blank=True)
    width = models.FloatField(null=True, blank=True)
    materail = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        default_permissions = ()


class VariationsHeader(Activity):
    attribute = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "variations_header"
        db_table = "variations_header"


class VariationsDetail(Activity):
    variation = models.ForeignKey(
        VariationsHeader,
        on_delete=models.CASCADE,
        related_name='variations')
    value = models.CharField(max_length=255)

    class Meta:
        default_permissions = ()
        verbose_name = "variations_detail"
        db_table = "variations_detail"


class Item(Activity):
    # General
    image = models.ImageField(
        upload_to=path_and_rename,
        default='default-product.jpg',
        blank=True,
        null=True)
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[(
        'template', 'Template'), ('variant', 'Variant'), ('standalone', 'Standalone')],
                            default='standalone', db_default='standalone', null=True, blank=True)
    sku_code = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True)
    barcode_type = models.CharField(max_length=255, null=True, blank=True)
    barcode = models.CharField(
        max_length=255, null=True, unique=True, blank=True)
    type = models.CharField(max_length=255, choices=[('product', 'Product'), (
        'service', 'Service')], default='product', db_default='product')
    # usage have Raw Material, Goods, Works
    usage = models.CharField(max_length=255, choices=[('goods', 'Goods'), (
        'raw_material', 'Raw Material'), ('works', 'Works'), ('service', 'Service')], null=True, blank=True)
    variant_of = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True, related_name='variant_of_item')
    unit_of_measure = models.ManyToManyField(UnitOfMeasurment, blank=True)
    tags = models.ManyToManyField(Tags, null=True, blank=True)
    family = models.ForeignKey(
        ItemFamily,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    brand = models.ForeignKey(
        ItemBrand,
        null=True,
        blank=True,
        on_delete=models.PROTECT)
    category = models.ForeignKey(
        ItemCategory,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name='item_category')
    specs = models.ManyToManyField(Specs, blank=True)

    is_variant = models.BooleanField(default=False)
    tracking_stock_by_variant = models.BooleanField(default=False)
    variations = models.ManyToManyField(
        VariationsDetail, related_name='item_variations', blank=True)
    selected_variations = models.ManyToManyField(
        VariationsDetail, blank=True)
    alternative_items = models.ManyToManyField(
        to='self', blank=True, symmetrical=False)
    returnable_item = models.BooleanField(default=False, db_default=False)

    # Logistics
    width = models.FloatField(null=True, blank=True)
    width_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='width_unit')

    height = models.FloatField(null=True, blank=True)
    height_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='height_unit')

    length = models.FloatField(null=True, blank=True)
    length_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='length_unit')

    weight = models.FloatField(null=True, blank=True)
    weight_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='weight_unit')

    # pos
    available_in_pos = models.BooleanField(default=False, db_default=False)
    shelf_life = models.CharField(max_length=255, null=True, blank=True)
    end_of_life = models.CharField(max_length=255, null=True, blank=True)

    # sale
    allow_Sales = models.BooleanField(
        default=True, db_default=True)  # to be removed
    allow_sales = models.BooleanField(default=True, db_default=True)
    max_discount_Sales = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)  # to be removed
    max_discount_sales = models.DecimalField(
        max_digits=6, decimal_places=3, null=True, blank=True)
    default_sale_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        max_length=255,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='default_sales_unit')
    default_selling_price = models.DecimalField(max_digits=50, decimal_places=35,
                                                default=0, db_default=0, null=True, blank=True)  # in company currency
    default_selling_price_usd = models.DecimalField(max_digits=50, decimal_places=25,
                                                    default=0, db_default=0, null=True, blank=True)  # in usd currency

    # purchase
    default_cost = models.DecimalField(max_digits=50, decimal_places=25,
                                       default=0, db_default=0, null=True, blank=True)  # in company currency
    default_cost_usd = models.DecimalField(max_digits=50, decimal_places=25,
                                           default=0, db_default=0, null=True, blank=True)  # in usd currency
    lead_time = models.CharField(max_length=255, null=True, blank=True)
    minimum_quantity_order = models.FloatField(null=True, blank=True)
    default_purchase_unit_of_measure = models.ForeignKey(
        UnitOfMeasurment,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='default_purchase_unit')

    # inventory
    minimum_quantity_in_stock = models.FloatField(null=True, blank=True)
    warranty_period = models.CharField(max_length=255, null=True, blank=True)
    allow_negative_stock = models.BooleanField(default=False, db_default=False)
    auto_reorder = models.BooleanField(default=False, db_default=False)

    # Accounting
    # taxes = models.ManyToManyField(Taxes, blank=True)

    def save(self, *args, **kwargs):
        fields_to_round = ['default_selling_price',
                           'default_selling_price_usd', 'default_cost', 'default_cost_usd']

        for field_name in fields_to_round:
            field_value = getattr(self, field_name)
            if field_value is not None:
                field_value = Decimal(field_value)
                rounded_value = round_value(field_value)
                setattr(self, field_name, rounded_value)

        if self.tracking_stock_by_variant:
            self.role = 'template'
        elif self.variant_of is not None:
            self.role = 'variant'
        elif self.variant_of is None and not self.tracking_stock_by_variant:
            self.role = 'standalone'

        super(Item, self).save(*args, **kwargs)


class ItemPackage(Activity):
    item = models.ForeignKey(Item, null=True, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, null=True, on_delete=models.Case)
    quantity = models.FloatField(default=1)
    barcode = models.CharField(max_length=255)

    class Meta:
        default_permissions = ()
    #     verbose_name = "item_package"
    #     db_table  = "item_package"



class Warehouse(Activity):
    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255)
    branch = models.IntegerField(blank=True, null=True)
    item = models.ManyToManyField(Item, through='Itemswarehouse', blank=True)
    initial_Data = models.BooleanField(default=False)
    default = models.BooleanField(default=False)
    show_room = models.BooleanField(default=False, db_default=False)

    class Meta:
        unique_together = ("branch_id", "name")
        verbose_name_plural = "warehouse"
        db_table = "warehouse"

    def __str__(self):
        return self.name + " in " + str(self.branch)


class Itemswarehouse(Activity):
    warehouse = models.ForeignKey(
        Warehouse,
        on_delete=models.PROTECT,
        null=True,
        blank=True)
    area = models.JSONField(default=list)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
    quantity = models.FloatField(db_default=0, default=0)
    net_movement = models.FloatField(db_default=0, default=0)
    quantity_reserved = models.FloatField(db_default=0, default=0)

    branch = models.IntegerField(null=True, blank=True)
    opening = models.BooleanField(default=False)
    opening_quantity = models.IntegerField(default=0)
    stock_quantity = models.GeneratedField(
        expression=models.F("opening_quantity") + models.F("net_movement"),
        output_field=models.FloatField(),
        db_persist=True,
    )
    available_for_sale = models.GeneratedField(
        expression=models.F("opening_quantity") + models.F("net_movement") -
                   models.F("quantity_reserved"),
        output_field=models.FloatField(),
        db_persist=True,
    )

    def __str__(self):
        if self.warehouse:
            return str(self.quantity) + " " + self.item.name + " in " + \
                self.warehouse.name + " in branch" + str(self.branch)
        else:
            return str(self.quantity) + " " + self.item.name + \
                " in branch" + str(self.branch)

    class Meta:
        unique_together = ("item", "branch", "warehouse")
        default_permissions = ()
