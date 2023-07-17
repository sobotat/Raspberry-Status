## Small Script to show stats about CPU temp and load of raspberry with Rainbow Hat led board

- **Btn A** = Temp
- **Btn B** = Load
- **Btn C** = Off

### Run in background
```bash
    nohup sudo python -u main.py > "output.log" 2>&1 < /dev/null &
```

### Turn Off
```
    ps ax | grep main.py
    kill pID
```
