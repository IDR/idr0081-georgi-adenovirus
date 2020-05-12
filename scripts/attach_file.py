import argparse
import omero.clients
import omero.cli

MIMETYPE = 'text/csv'
NAMESPACE = 'openmicroscopy.org/idr/analysis/original'

def main(conn, filepath, target, mime, ns):
  try:
    ot,oid = target.split(":")
  except:
     print("Could not parse target specification")

  tgt = conn.getObject(ot, int(oid))
  fo = conn.createOriginalFileFromLocalFile(filepath, mimetype=mime, ns=ns)
  fa = omero.model.FileAnnotationI()
  fa.setFile(fo._obj)
  fa.setNs(omero.rtypes.rstring(NAMESPACE))
  fa = conn.getUpdateService().saveAndReturnObject(fa)
  fa = omero.gateway.FileAnnotationWrapper(conn, fa)
  tgt.linkAnnotation(fa)

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument("file", help="The file to attach.")
  parser.add_argument("target", help="The target to attach the file to.")
  parser.add_argument("--mime", help="The mime type. Default: text/csv")
  parser.add_argument("--ns", help="The name space. Default: openmicroscopy.org/idr/analysis/original")

  args = parser.parse_args()
  mime = MIMETYPE if not args.mime else args.mime
  ns = NAMESPACE if not args.ns else args.ns

  with omero.cli.cli_login() as c:
    conn = omero.gateway.BlitzGateway(client_obj=c.get_client())
    main(conn, args.file, args.target, mime, ns)
