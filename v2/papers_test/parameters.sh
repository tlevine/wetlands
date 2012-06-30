#!/bin/sh

. papers.sh

runtests() {
  assert 'paper function errors when type is not public_notice or drawing' false
  assert 'paper function passes when type is public_notice' false
  assert 'paper function passes when type is drawing' false
}
