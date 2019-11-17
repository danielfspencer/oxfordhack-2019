cp samples/* ../compose/png
cd ../compose
make clean
make -j 4
rm png/*
cp NotoColorEmoji.ttf ../tester/test.ttf
echo ""
echo " --- open test.html in chrome/chromium --- "
