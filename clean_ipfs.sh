sudo -u ipfs IPFS_PATH=/home/ipfs/.ipfs ipfs pin ls --type=recursive -q \
  | xargs -n1 -I{} sudo -u ipfs IPFS_PATH=/home/ipfs/.ipfs ipfs pin rm {}
