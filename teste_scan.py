import subprocess

dispositivos = []
ip_fix = "192.168.1."
for i in range(1, 255):
    i = str(i)
    ip_teste = ip_fix + i
    ip = subprocess.run(["ping", "-c", "1", "-W", "1", ip_teste], stdout=subprocess.DEVNULL)

    if ip.returncode == 0:
        dispositivos.append(ip_teste)

print(dispositivos)