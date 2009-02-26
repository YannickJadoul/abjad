from abjad.rational.rational import Rational
import math

def interpolate_cosine(y1, y2, mu):
   '''
   Cosine interpolation.
   mu is normalized [0, 1].
   '''
   mu2 = (1 - math.cos(mu * math.pi)) / 2
   return (y1 * (1 - mu2) + y2 * mu2)


def interpolate_linear(y1, y2, mu):
   '''
   Linear interpolation.
   mu is normalized [0, 1].
   '''
   return (y1 * (1 - mu) + y2 * mu)


def interpolate_exponential(y1, y2, mu, exp=1):
   '''
   Linear interpolation.
   mu is normalized [0, 1].
   '''
   return (y1 * (1 - mu ** exp) + y2 * mu ** exp)


def interpolate_divide(total, start_frac, stop_frac, exp='cosine'):
   '''
   Divide total into segments of sizes computed from interpolating 
   between start_frac and stop_frac. 
   Set exp='cosine' for cosine interpolation. This is the default. If set
   to a numeric value, the interpolation is exponential and exp is the 
   exponent.
   '''
   result =  [ ]
   ip = 0
   cumulative = 0
   while cumulative <= total - stop_frac:
      if exp == 'cosine':
         ip = interpolate_cosine(start_frac, stop_frac,
            cumulative / total)
      else:
         ip = interpolate_exponential(start_frac, stop_frac,
            cumulative / total, exp)
      ip = int(round(ip * 10000, 5))
      ip = Rational(ip, 10000)
      result.append(ip)
      cumulative += ip
   residue = total - cumulative
   result[-1] += residue
   return result


