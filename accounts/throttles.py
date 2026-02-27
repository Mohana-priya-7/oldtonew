from rest_framework.throttling import SimpleRateThrottle
#OTPThrottle → Inherits → SimpleRateThrottleMeaning:It already has throttling logic built-in.
class OTPThrottle(SimpleRateThrottle):
    scope = 'otp'  #Scope connects this throttle to settings.py.Scope name = "otp"
    def get_cache_key(self, request, view):
        return self.get_ident(request)  #get_ident gives us the unique identifier for the user making the request.Usually, it's the IP address of the user. This means that the throttling will be applied based on the user's IP address.Each IP gets 3 requests per minute Different IP → separate count
    
#Without throttle:Attacker can do:POST /forgot-password/ 1000 times per minute.

#Result:Email spam,Server overload,Security issue.With throttle:Max 3 per minute per IP.    