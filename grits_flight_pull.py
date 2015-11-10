import ftplib
import os
import hashlib
import zipfile

from grits_ftp_config import url, uname, pwd

def sortByModified( aString ):
    entryAttr = aString.split(';')
    modified = entryAttr[2].strip()
    return modified

def md5Checksum(filePath):
    with open(filePath, 'rb') as fh:
        m = hashlib.md5()
        while True:
            data = fh.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

print "Connecting to Innovata"
f = ftplib.FTP()
f.connect(url)
f.login(uname, pwd)
ls = []
f.retrlines('MLSD', ls.append)  

#sort decending, latest now first. Loop through list until we get to the newest zip file.
ls.sort( key= sortByModified, reverse= True )
for entry in ls:

    entryAttr = entry.split(";")
    filename = entryAttr[3].strip()
    
    #EcoHealth_20151102  .zip or .md5
    name, extension = os.path.splitext(entryAttr[3])
    
    #Stop at first/newest .zip file, this contains our deliverable
    if extension == '.zip':
      print "Most recent zip file deliverable: %s" % name

      #now get all the items containing filename, but ending in md5, make sure MD5 exists
      containsMD5 = [s for s in ls if name + '.md5' in s]
      if len(containsMD5) != 1:
        raise IOError("ERROR: Corresponding MD5 not found for latest deliverable %s" % name)

      #Current MD5 digest
      md5filename = containsMD5[0].split(";")[3].strip()

      #Create, use data directory relative to current directory for zip deliverable 
      data_directory = os.path.join( os.getcwd(), 'data')
      if not os.path.exists(data_directory):
        os.makedirs(data_directory)
      print "Data directory %s" % data_directory 

      filepathname = os.path.join(data_directory, filename)
      try:
        fileOut = open(filepathname,'wb')
      except:
        raise IOError("ERROR: Could not open the output file for writing")

      print "Downloading ZIP file to: %r" % filepathname
      f.retrbinary('RETR %s' % filename, fileOut.write)
      fileOut.close()

      #Open the zip file, check that there is only one file inside, should be just one CSV
      zip_ref = zipfile.ZipFile(filepathname, 'r')
      if len(zip_ref.namelist()) != 1:
        raise IOError("ERROR: More than one file contained in Zip, should just be one CSV file")

      #Extract the zip, with just one file
      print "Extracting zip file: %s" % zip_ref.namelist()[0]
      csvfile = zip_ref.extract(zip_ref.namelist()[0], data_directory)
      zip_ref.close()
      print "Deliverable CSV: %r" % csvfile
      
      #Compute MD5 digest
      csv_digest = md5Checksum(csvfile).strip()
      md5filepathname = os.path.join(data_directory, md5filename)
      try:
        #Write, and in binary mode
        fileOutMD5 = open(md5filepathname,'wb')
      except:
        raise IOError("ERROR: Could not open the output MD5 for writing")

      print "Downloading MD5 digest file to %s" % md5filepathname
      f.retrbinary('RETR %s' % md5filename, fileOutMD5.write)
      fileOutMD5.close()

      try:
        #Open the file for reading
        fileMD5 = open(md5filepathname,'r')
      except:
        raise IOError("ERROR: Could not open the md5 file for reading")

      md5_digest = fileMD5.readline().strip()
      fileMD5.close()
      f.close()

      if md5_digest.lower() == csv_digest.lower():
        print "MD5 digest match, file is good"
      else:
        print 'md5_digest: [%s]' % md5_digest.lower()
        print 'csv_digest: [%s]' % csv_digest.lower()
        
        raise IOError("ERROR: Corrupt download, or corrupt file! MD5 doesn't match. Please try again.")

      print "Done"
      break
