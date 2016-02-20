START=$(date +%s)
for (( i = 0 ; i < 40000; i++ ))
do
    mysql -uadmin_gale_ru -padmin_gale_ru admin_test_gale_ru < insert.sql
done
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "It took $DIFF seconds"