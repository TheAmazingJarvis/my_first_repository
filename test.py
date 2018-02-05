# read the field files
fields_source_1 = fields.read_fields(fields_source_1_file)
fields_source_2 = fields.read_fields(fields_source_2_file)
addon_fields = fields.read_fields(addon_fields_file)
field_name_mastr = fields_source_1 + fields_source_2 + addon_fields
number_of_fields = len(field_name_mastr)

scraped_field_values    all addon field values
scraped_field_names     all addon field names
merged_lists_1          all scraped fields and names - two dimmensional
pruned_list_1           only requested fields - two dimmensional

