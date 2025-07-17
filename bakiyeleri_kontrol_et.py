import requests
import time

def adresleri_oku(dosya_adi):
    with open(dosya_adi, 'r') as f:
        adresler = [satir.strip() for satir in f if satir.strip()]
    return adresler

def trx_bakiyesi(adres):
    url = f'https://apilist.tronscanapi.com/api/account?address={adres}'
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        return float(data.get('balance', 0)) / 1_000_000
    except Exception as e:
        print(f"{adres} için TRX bakiyesi alınamadı: {e}")
        return None

def usdt_bakiyesi(adres):
    url = f'https://apilist.tronscanapi.com/api/account?address={adres}'
    try:
        r = requests.get(url, timeout=10)
        data = r.json()
        for token in data.get('trc20token_balances', []):
            if token.get('tokenAbbr') == 'USDT':
                return float(token.get('balance', 0)) / 1_000_000
        return 0.0
    except Exception as e:
        print(f"{adres} için USDT bakiyesi alınamadı: {e}")
        return None

def main():
    adresler = adresleri_oku('adresler.txt')
    print(f"Toplam {len(adresler)} adres bulundu.\n")
    for adres in adresler:
        trx = trx_bakiyesi(adres)
        usdt = usdt_bakiyesi(adres)
        print(f"Adres: {adres}")
        print(f"  TRX:  {trx if trx is not None else 'Hata':.6f}")
        print(f"  USDT: {usdt if usdt is not None else 'Hata':.6f}\n")
        time.sleep(1)  # API'yi yormamak için bekleme

if __name__ == '__main__':
    main() 