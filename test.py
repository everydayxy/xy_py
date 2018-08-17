import hmac

h = hmac.new('含笑'.encode('utf-8'),'如花'.encode('utf-8'))
print(h.digest())