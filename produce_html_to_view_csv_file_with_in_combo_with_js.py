#!/usr/bin/env python
import os
"""
	you will need to have dygraph-combined.js in the same directory
	(on your web server) as the html generated via this script for the
	charts to work ^^
"""

if __name__ == "__main__":
	csv_files = [i for i in os.listdir(".") if i.endswith(".csv")]
	csv_files.sort()

	print """<html>
        	<head>
	                <script type="text/javascript" src="dygraph-combined.js"></script>
			        </head>
				        <body>
	"""
	for file_name in csv_files:
		mod_file_name = file_name.replace(".csv", "").replace("-", "").replace(".","")
		temp_html = '''
                <div id="'''+ mod_file_name + '''" style="width:1000px; height:500px;"></div>
                <script type="text/javascript">
                '''+ mod_file_name +'''= new Dygraph(\ndocument.getElementById("'''+ mod_file_name + '''"),\n"'''+ file_name +'''", // path to CSV file
                                { colors: ['#EE1111']}          // options
                                                );
                </script>'''
		print file_name
		print temp_html

	print """
	</body>
	</html>
	"""

