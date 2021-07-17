#!/usr/bin/env bash

cd "${0%/*}"
rm -f FilamentLoadCell.zip
zip -r FilamentLoadCell.zip dsf/ dwc/ plugin.json
