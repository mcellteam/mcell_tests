
find . \( -type d -name .git -prune \) -o -type f -print0 | xargs -0 sed -i 's/MCELL_PATH/MCELL_PATH/g'
