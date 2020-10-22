
#find . -name "*.py" -type -f -print0 | xargs -0 sed -i 's/element_connections/wall_list/g'

find . -name "*.py" -type f -print0 | xargs -0 sed -i 's/element_connections/wall_list/g'

#find . -type f -print0 | xargs -0 sed -i 's/element_connections/wall_list/g'
