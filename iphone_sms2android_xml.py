#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
Tool to convert iPhone SMS database to XML format,
which can be imported by Android application.
Inspired by http://semplicewebsites.com/copy-sms-text-messages-iphone-to-android
Unfortunately, article was written in 2011, and iOS7 has slightly changed
structure, so I had to improvise.
"""
import lxml.etree as ET
import sqlite3
import sys

TIMESPAN = 978307200000 # we want correct dates

def main():
    """ Do the magic! """
    database_name = output_xml = ''
    if len(sys.argv) == 3:
        database_name = sys.argv[1]
        output_xml = sys.argv[2]
    else:
        database_name = '3d0d7e5fb2ce288813306e4d4636395e047a3d28'
        output_xml = 'sms.xml'

    try:
        root = ET.Element('smses')

        database = sqlite3.connect(database_name)

        cur = database.cursor()
        cur.execute("""
            SELECT H.id AS address, M.date, M.is_from_me, M.text
            FROM message M LEFT JOIN handle H ON M.handle_id=H.rowid
        """)

        rows = cur.fetchall()

        i = 0

        for row in rows:
            sms = ET.SubElement(root, 'sms')
            sms.set('protocol', '0')
            sms.set('address', str(row[0]))
            sms.set('date', str(row[1] * 1000 + TIMESPAN))
            sms.set('type', '2' if row[2] == 1 else '1')
            sms.set('subject', '')
            sms.set('body', row[3] if row[3] is not None else '')
            sms.set('toa', '0')
            sms.set('sc_toa', '0')
            sms.set('service_center', '0')
            sms.set('read', '1')
            sms.set('status', '-1')
            i += 1

        root.set('count', str(i))

    finally:
        if database:
            database.close()

        tree = ET.ElementTree(root)
        tree.write(output_xml,
                   xml_declaration=True,
                   encoding='utf-8',
                   pretty_print=True,
                   method='xml')

if __name__ == '__main__':
    main()
