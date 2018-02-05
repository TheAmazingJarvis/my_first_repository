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

        #
        #   start saving the data
        #
        #
        number_of_scraped_fields = len(scraped_field_names)
        scraped_data = merge_lists(scraped_field_names, scraped_field_values)
        extra_fields = list(scraped_data)  # in scraped_values but NOT in master_fields

        #
        # customize the weight and dimensions
        #
        index = 0
        for field, value in scraped_data:
            # print('Index: {}   Field: {}   Value: {}'.format(index, field, value))
            if field == 'weight (inc. batteries)'.strip():
                i = value.find('g')
                value = value[:i]
                # scraped_data.append(['dimensions-weight', value])
                scraped_data[index][1] = value
            elif field == 'normal focus range':
                i = value.find('cm')
                value = value[:i]
                # scraped_data.append(['minimum-focus', value])
                scraped_data[index][1] = value
            elif field == 'macro focus range':
                i = value.find('cm')
                value = value[:i]
                # scraped_data.append(['minimum-focus', value])
                scraped_data[index][1] = value
            elif field == 'dimensions':
                scraped_data[index][1] = ''
                i = value.find('mm')
                value = value[:i]
                h, w, d = value.split(' x ')
                scraped_data.append(['dimensions-height', h])
                scraped_data.append(['dimensions-width', w])
                scraped_data.append(['dimensions-depth', d])
            index += 1

        not_found_fields = list(field_name_mastr)  # not in scraped_values but ARE IN master_fields

        log.main(str(number_of_scraped_fields) + ' of ' + str(number_of_fields) + ' fields found.')

        # print('\nnumber_of_scraped_fields ', str(number_of_scraped_fields))
        # print('field_name_mastr ', str(len(field_name_mastr)), field_name_mastr)
        # print('not_found_fields ', str(len(not_found_fields)), not_found_fields)
        # print('scraped_data ', str(len(scraped_data)), scraped_data)
        # print('extra_fields ', str(len(extra_fields)), extra_fields)
        # print()

        for i in field_name_mastr:
            for field, value in scraped_data:
                if i == field:
                    found_values.append(i)
                    try:
                        extra_fields.remove([field, value])
                    except:
                        # print('field: ' + field + '\ni:     ' + i + '\nValue: ' + value)
                        log.main('Weirdism (duplicate?): ' + i)
                        log.source(log_name, 'Weirdism (duplicate?): ' + i)
                    try:
                        # this is here because sometimes a field will be in a page more than once
                        not_found_fields.remove(i)
                    except:
                        log.main('Found extra field: ' + i)
                        log.source(log_name, 'Found extra field: ' + i)

        scraped_data_proc = dict(scraped_data)
        intermed_output = [[k, scraped_data_proc[k]] if k in scraped_data_proc else [None, None] for k in
                           field_name_mastr]

        # print('intermed_output ', intermed_output)

        for x, y in intermed_output:
            final_output.append(y)
        save.save_record(final_output)

        # print('\nnumber_of_scraped_fields ', str(number_of_scraped_fields))
        # print('field_name_mastr ', str(len(field_name_mastr)), field_name_mastr)
        # print('not_found_fields ', str(len(not_found_fields)), not_found_fields)
        # print('scraped_data ', str(len(scraped_data)), scraped_data)
        # print('extra_fields ', str(len(extra_fields)), extra_fields)
        # print()
        #
        # print('\nfinal_output', final_output)

        log.source(log_name, str(line_number) + "-" + url)
        log.source(log_name, 'Product Title: ' + product_name)
        log.source(log_name, '       Fields:\n' + str(field_name_mastr))
        log.source(log_name, '\nScraped Fields:\n' + str(scraped_data))
        log.source(log_name, '\nShared Fields saved to csv:\n' + str(found_values))
        log.source(log_name, '\nMissing Fields - these are in the Master list '
                             'but not the Scraped List:\n' + str(not_found_fields))
        log.source(log_name, '\nLeft Over Fields not saved to csv - these where in '
                             'the Scraped List but not the Master List:\n' + str(extra_fields))

        time_scrape_stop = datetime.datetime.now()
        time_scrape_total = time_scrape_stop - time_scrape_start

        log.main('Completed ' + str(line_number) + '-' + url.strip())
        log.main('Time to complete: ' + str(time_scrape_total))
        log.main('')
        line_number += 1
