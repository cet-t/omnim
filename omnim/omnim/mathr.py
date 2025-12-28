import ctypes
import math
from pathlib import Path
from typing import Final


try:
    _dir = Path(__file__).parent.absolute()
    _dll = _dir / "omnim_math_rust.dll"
    if not _dll.exists():
        raise FileExistsError()
    _lib = ctypes.cdll.LoadLibrary(str(_dll))

    class _Complex(ctypes.Structure):
        _fields_ = [("re", ctypes.c_double), ("im", ctypes.c_double)]

        def to_complex(self) -> complex:
            return complex(self.re, self.im)

    HAS_RUST = True
except:
    HAS_RUST = False


if HAS_RUST:
    _lib.pi.restype = ctypes.c_double

    _lib.e.restype = ctypes.c_double

    _lib.eps.restype = ctypes.c_double

    _lib.golden_ratio.restype = ctypes.c_double

    _lib.approximately.argtypes = [ctypes.c_double, ctypes.c_double]
    _lib.approximately.restype = ctypes.c_bool

    _lib.to_degrees.argtypes = [ctypes.c_double]
    _lib.to_degrees.restype = ctypes.c_double

    _lib.to_radians.argtypes = [ctypes.c_double]
    _lib.to_radians.restype = ctypes.c_double

    _lib.factor.argtypes = [ctypes.c_longlong]
    _lib.factor.restype = ctypes.c_longlong

    _lib.mini.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_size_t]
    _lib.mini.restype = ctypes.c_longlong

    _lib.minf.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
    _lib.minf.restype = ctypes.c_double

    _lib.maxi.argtypes = [ctypes.POINTER(ctypes.c_longlong), ctypes.c_size_t]
    _lib.maxi.restype = ctypes.c_longlong

    _lib.maxf.argtypes = [ctypes.POINTER(ctypes.c_double), ctypes.c_size_t]
    _lib.maxf.restype = ctypes.c_double

    _lib.clampi.argtypes = [ctypes.c_longlong, ctypes.c_longlong, ctypes.c_longlong]
    _lib.clampi.restype = ctypes.c_int

    _lib.clampf.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_double]
    _lib.clampf.restype = ctypes.c_double

    _lib.signi.argtypes = [ctypes.c_longlong]
    _lib.signi.restype = ctypes.c_int

    _lib.signf.argtypes = [ctypes.c_double]
    _lib.signf.restype = ctypes.c_double

    _lib.absi.argtypes = [ctypes.c_longlong]
    _lib.absi.restype = ctypes.c_longlong

    _lib.absf.argtypes = [ctypes.c_double]
    _lib.absf.restype = ctypes.c_double

    _lib.floori.argtypes = [ctypes.c_longlong, ctypes.c_longlong]
    _lib.floori.restype = ctypes.c_longlong

    _lib.floorf.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.floorf.restype = ctypes.c_double

    _lib.round.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.round.restype = ctypes.c_double

    _lib.ceil.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.ceil.restype = ctypes.c_double

    _lib.powi.argtypes = [ctypes.c_longlong, ctypes.c_longlong]
    _lib.powi.restype = ctypes.c_longlong

    _lib.powf.argtypes = [ctypes.c_double, ctypes.c_double]
    _lib.powf.restype = ctypes.c_double

    _lib.sqrt.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.sqrt.restype = ctypes.c_double

    _lib.sin.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.sin.restype = ctypes.c_double

    _lib.cos.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.cos.restype = ctypes.c_double

    _lib.tan.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.tan.restype = ctypes.c_double

    _lib.asin.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.asin.restype = ctypes.c_double

    _lib.acos.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.acos.restype = ctypes.c_double

    _lib.atan.argtypes = [ctypes.c_double, ctypes.c_longlong]
    _lib.atan.restype = ctypes.c_double

    _lib.atan2.argtypes = [ctypes.c_double, ctypes.c_double, ctypes.c_longlong]
    _lib.atan2.restype = ctypes.c_double

    _lib.is_prime.argtypes = [ctypes.c_longlong]
    _lib.is_prime.restype = ctypes.c_bool

    _lib.fibonacci.argtypes = [ctypes.c_longlong]
    _lib.fibonacci.restype = ctypes.c_int

    pi: Final[float] = _lib.pi()
    e: Final[float] = _lib.e()
    eps: Final[float] = _lib.eps()
    golden_ratio: Final[float] = _lib.golden_ratio()

    def approximately(a: float, b: float) -> bool:
        return _lib.approximately(a, b)

    def to_degrees(x: float) -> float:
        return _lib.to_degrees(x)

    def to_radians(x: float) -> float:
        return _lib.to_radians(x)

    def factor(n: int) -> int:
        return _lib.factor(n)

    def factorf(n: int) -> float:
        return _lib.factorf(n)

    def mini(*xs: int) -> int:
        src_len = len(xs)
        src_type = ctypes.c_longlong * src_len
        src_array = src_type(*xs)
        return _lib.mini(src_array, src_len)

    def minf(*xs: float) -> float:
        src_len = len(xs)
        src_type = ctypes.c_double * src_len
        src_array = src_type(*xs)
        return _lib.minf(src_array, src_len)

    def maxi(*xs: int) -> int:
        src_len = len(xs)
        src_type = ctypes.c_longlong * src_len
        src_array = src_type(*xs)
        return _lib.maxi(src_array, src_len)

    def maxf(*xs: float) -> float:
        src_len = len(xs)
        src_type = ctypes.c_double * src_len
        src_array = src_type(*xs)
        return _lib.maxf(src_array, src_len)

    def clampi(x: int, min_value: int, max_value: int) -> int:
        return _lib.clampi(x, min_value, max_value)

    def clampf(x: float, min_value: float, max_value: float) -> float:
        return _lib.clampf(x, min_value, max_value)

    def signi(x: int) -> int:
        return _lib.signf(x)

    def signf(x: float) -> float:
        return _lib.signi(x)

    def absi(x: int) -> int:
        return _lib.absi(x)

    def absf(x: float) -> float:
        return _lib.absf(x)

    def floori(x: int, d=0) -> int:
        return _lib.floori(x, d)

    def floorf(x: float, d=0) -> float:
        return _lib.floorf(x, d)

    def round(x: float, d=0) -> float:
        return _lib.round(x, d)

    def ceil(x: float, d=0) -> float:
        return _lib.ceil(x, d)

    def powi(x: int, exp: int) -> int:
        return _lib.powi(x, exp)

    def powf(x: float, exp: float) -> float:
        return _lib.powf(x, exp)

    def sqrt(x: float, term=10) -> float:
        return _lib.sqrt(x, term)

    def sin(x: float, term=5) -> float:
        return _lib.sin(x, term)

    def cos(x: float, term=5) -> float:
        return _lib.cos(x, term)

    def tan(x: float, term=10) -> float:
        return _lib.tan(x, term)

    def asin(x: float, term=10) -> float:
        return _lib.asin(x, term)

    def acos(x: float, term=10) -> float:
        return _lib.acos(x, term)

    def atan(x: float, term=10) -> float:
        return _lib.atan(x, term)

    def atan2(y: float, x: float, term=10) -> float:
        return _lib.atan2(y, x, term)

    def is_prime(n: int) -> bool:
        return _lib.is_prime(n)

    def fibonacci(n: int) -> int:
        return _lib.fibonacci(n)

    def eix(x: float, term=10):
        return cos(x, term) + (1j * sin(x, term))


if __name__ == "__main__":
    print(f"{HAS_RUST=}")
    print(f"{pi=}")
    print(f"{e=}")
    print(f"{eps=}")
    print(f"{golden_ratio=}")
    print(f"{approximately(0, 1)=}")
    print(f"{to_degrees(0)=}")
    print(f"{to_radians(0)=}")
    print(f"{factor(3)=}")
    print(f"{factorf(3)=}")
    print(f"{mini(*[1, 2, 3])=}")
    print(f"{maxi(*[1, 2, 3])=}")
    print(f"{minf(*[1, 2, 3])=}")
    print(f"{maxf(*[1, 2, 3])=}")
    print(f"{clampi(100, 1, 99)=}")
    print(f"{clampi(0, 1, 99)=}")
    print(f"{clampf(100, 1, 99)=}")
    print(f"{clampf(0, 1, 99)=}")
    print(f"{signi(+12)=}")
    print(f"{signf(-12)=}")
    print(f"{signi(-0)=}")
    print(f"{signf(+0)=}")
    print(f"{absi(-12)=}")
    print(f"{absf(-0.99)=}")
    print(f"{absi(+12)=}")
    print(f"{absf(+0.99)=}")
    print(f"{floori(12, 0)=}")
    print(f"{floorf(12.3, 0)=}")
    print(f"{round(12, 0)=}")
    print(f"{ceil(12, 0)=}")
    print(f"{powi(2, 10)=}")
    print(f"{powf(2, 10)=}")
    print(f"{sqrt(2, 10)=}")
    x = to_radians(89)
    print(f"{sin(x)=:.3f}")
    print(f"{math.sin(x)=:.3f}")
    print(f"{cos(x)=:.3f}")
    print(f"{math.cos(x)=:.3f}")
    print(f"{tan(x)=:.3f}")
    print(f"{math.tan(x)=:.3f}")
    print(f"{asin(0, 20)=:.3f}")
    print(f"{math.asin(0)=:.3f}")
    print(f"{acos(0, 20)=:.3f}")
    print(f"{math.acos(0)=:.3f}")
    print(f"{atan(0, 20)=:.3f}")
    print(f"{math.atan(0)=:.3f}")
    print(f"{atan2(1, 1, 30)=}")
    print(f"{math.atan2(1, 1)=}")
    print(f"{is_prime(57)=}")
    print(f"{fibonacci(10)=}")

    print(f"{eix(pi).real=}")
