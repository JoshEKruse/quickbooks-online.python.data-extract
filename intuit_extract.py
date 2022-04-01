from intuitlib.client import AuthClient
from quickbooks import QuickBooks
from quickbooks.objects import Customer

auth_client = AuthClient(
    client_id = 'ABcWQcMeUTm1r9Qq209oSi8ZIvTJ47HpKPqDF3tOOqHiPKicKN',
    client_secret = 'QX7rR2fWdE0TEZbqi537OOYpLiKiSPd4D05xTK4d',
    access_token = 'eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..OpI10xst7h8zprKxyFfjuQ.q8x2wBTn9YgrytBA93w3L5RJ46CE3r_08bOL1R7QI_ffbw3YlTCYQDF3bBWpUA4b0cEwVlCDyMyz71jHWboMYiAZ0UXGHTn0FyuUnqkSSI7fNjogaJiFVH74Sk6-1Gg362ygfzmaH9JOvhG22jse-87pWeyb3NbP0zzO08hUilvXXk6BQXp1EceLtaHPdTsBvEXbcT18Y0lp99fuWyt40Iaa_z_CGO_aHYs0zqMLTguDFfut7zPVY8XJPTLX2scLa7b_QEhMWJOuAlM4zXzlWv6chXWKbjfrHHt2Mg6lKtsLRzciaUR-WUzAGbAERTXgiEYmpNcYYzcKg5SzSPy2XZK70dYu417IInqNTSHqvMhaR37pGkKN-ZuJoOeX-Hh2q6WFS-06E8nPel4JrGpIb9RpXrymYI5u5jIT7kPNcAIAZkI3O1ydg6idkRoCE7E8BYLlWkrsAZsu5jODN0jOSrR1rUN67PRwvmJWL9-D75nKYaVmAJrCBFMJdmjx6-3zIyJK2LfM0oFxDpFOhoWBmJ5-CiNY6tLu-dIon5GUqK0LoK96zGcaCG2SHdOlvtef_9F5yDiQToY89SwCtWxaI6woSr0UaGYq_F1bms5H2vYhyMalw3TtbwjgcuF_LskCIbnmRW5h87o8M_jl7z9Lc-M3QFZd7NT_ZQF6UGjIkJecyA-Sj41vBn7AhRsZKfT4Da--_jlfhnZd4BzIvGypTTOMF_4w33Nvz7tzEfEuqJs.f-dzxPxf4LFmJn8z0To1Mw',
    environment = 'sandbox',
    redirect_uri = 'https://developer.intuit.com/v2/OAuth2Playground/RedirectUrl',
)

client = QuickBooks(
    auth_client = auth_client,
    refresh_token = 'AB116575051291mhTRdac4N4fONdIneBnplsiAGgUPaLRW2Hmg',
    company_id = '4620816365217598370',
)

customers = Customer.all( qb=client )

print( customers )
