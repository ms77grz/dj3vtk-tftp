def sp(port_id):
    # slot/port mapping to OID port id
    data = {
        '4194304000': '0/0',
        '4194304256': '0/1',
        '4194304512': '0/2',
    }
    return data.get(port_id)