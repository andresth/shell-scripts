#!/bin/sh

set -e

for domain in $RENEWED_DOMAINS; do
  case $domain in
    andres.in)
      prosody_cert_root=/etc/prosody/certs/
      umask 077
      cp "$RENEWED_LINEAGE/fullchain.pem" "$prosody_cert_root/fullchain.pem"
      cp "$RENEWED_LINEAGE/privkey.pem" "$prosody_cert_root/privkey.pem"
      chown -R prosody:prosody "$prosody_cert_root"
      chmod -R 400 "prosody_cert_root"
      systemctl restart prosody.service > /dev/null
      ;;
  esac
done
