#!/bin/sh

. ./papers.sh

runtests() {
  assert 'paper function errors when type is not public_notice or drawing'\
    'paper --papertype=invalid --date=2012-04-01 --url=http://localhost:9001 --permit=MVN-foo-bar-baz'
# assert 'paper function passes when type is public_notice' false
# assert 'paper function passes when type is drawing' false
}
