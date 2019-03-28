# ardent_odrive
Motor controller code and documentation. 

```
git clone https://github.com/neomanic/ODrive -b py27compat
cd ODrive/tools
sudo pip install monotonic

# sudo python setup.py install # doesn't work due to weird setup process, so do the following:
python setup.py sdist
sudo pip install dist/odrive-0.4.4.dev0.tar.gz
```
