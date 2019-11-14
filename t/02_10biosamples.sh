#!/usr/bin/env bats

here=$BATS_TEST_DIRNAME
db=$here/test.sqlite
script=$here/../scripts/addFromNcbi.sh

@test "Add from NCBI" {
  BIOSAMPLE="SAMN02182865 SAMN02182866 SAMN02182867 SAMN02182868 SAMN02182869 SAMN02182870 SAMN02182871 SAMN02182872 SAMN02182873 SAMN02182874"
  [ 1 -eq 1 ];
  return;

  for i in $BIOSAMPLE; do
    echo "# $BIOSAMPLE" >&3
    run $script $db $BIOSAMPLE
    [[ "$status" -eq 0 ]] 
  done
}