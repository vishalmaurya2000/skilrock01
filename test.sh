#!/bin/bash

user=root
pass=redhat
host="abc,xyz"
#DB=
#date=date +%Y-%m-%d_%Hh%Mm

mysqldump -u$user -p$pass  $host > dump.$(date +%F)sql

#mysqldump --all-databases --single-transaction --quick --lock-tables=false > full-backup-$(date +%F).sql -u $user -p $pass



