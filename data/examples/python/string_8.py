from inline import itest

def _normalize(self, name, columns, points):
    """Normalize data for the InfluxDB's data model.

    :return: a list of measurements.
    """
    ret = []

    # Build initial dict by crossing columns and point
    data_dict = dict(zip(columns, points))

    # issue1871 - Check if a key exist. If a key exist, the value of
    # the key should be used as a tag to identify the measurement.
    keys_list = [k.split(".")[0] for k in columns if k.endswith(".key")]
    itest().given(columns, ["a.key", "b.key"]).check_eq(keys_list, ["a", "b"])

    if len(keys_list) == 0:
        keys_list = [None]

    for measurement in keys_list:
        # Manage field
        if measurement is not None:
            fields = {
                k.replace("{}.".format(measurement), ""): data_dict[k]
                for k in data_dict
                if k.startswith("{}.".format(measurement))
            }
        else:
            fields = data_dict
        # Transform to InfluxDB datamodel
        # https://docs.influxdata.com/influxdb/v2.0/reference/syntax/line-protocol/
        for k in fields:
            #  Do not export empty (None) value
            if fields[k] is None:
                continue
            # Convert numerical to float
            try:
                fields[k] = float(fields[k])
            except (TypeError, ValueError):
                # Convert others to string
                try:
                    fields[k] = str(fields[k])
                except (TypeError, ValueError):
                    pass
        # Manage tags
        tags = self.parse_tags(self.tags)
        if "key" in fields and fields["key"] in fields:
            # Create a tag from the key
            # Tag should be an string (see InfluxDB data model)
            tags[fields["key"]] = str(fields[fields["key"]])
            # Remove it from the field list (can not be a field and a tag)
            fields.pop(fields["key"])
        # Add the hostname as a tag
        tags["hostname"] = self.hostname
        # Add the measurement to the list
        ret.append({"measurement": name, "tags": tags, "fields": fields})
    return ret
