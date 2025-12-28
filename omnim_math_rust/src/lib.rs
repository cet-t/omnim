#[unsafe(no_mangle)]
pub extern "C" fn pi() -> f64 {
    4. * (4. * atan(1. / 5., 30) - atan(1. / 239., 30))
}

#[unsafe(no_mangle)]
pub extern "C" fn e(term: i64) -> f64 {
    let mut res = 1.0;
    let mut factory = 1.0;
    for n in 1..term.abs().min(30) {
        factory *= n as f64;
        res += 1.0 / factory;
    }
    res
}

#[unsafe(no_mangle)]
pub extern "C" fn eps() -> f64 {
    1. - (((4. / 3.) - 1.) + ((4. / 3.) - 1.) + ((4. / 3.) - 1.))
}

#[unsafe(no_mangle)]
pub extern "C" fn golden_ratio() -> f64 {
    (1. + sqrt(5., 10)) / 2.
}

#[unsafe(no_mangle)]
pub extern "C" fn approximately(a: f64, b: f64, tolerant: f64) -> bool {
    absf(a - b) <= tolerant
}

#[unsafe(no_mangle)]
pub extern "C" fn to_degrees(x: f64) -> f64 {
    x * (180.0 / pi())
}

#[unsafe(no_mangle)]
pub extern "C" fn to_radians(x: f64) -> f64 {
    x * (pi() / 180.0)
}

#[unsafe(no_mangle)]
pub extern "C" fn factor(n: i64) -> i64 {
    if n <= 1 {
        1
    } else {
        (1..=n).map(|i| i).product()
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn factorf(n: i64) -> f64 {
    if n <= 1 {
        1.0
    } else {
        (1..=n).map(|i| i as f64).product()
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn mini(ptr: *const i64, len: usize) -> i64 {
    if len == 0 {
        return 0;
    }

    let xs = unsafe { std::slice::from_raw_parts(ptr, len) };

    let mut min = xs[0];
    for &x in xs {
        if x < min {
            min = x;
        }
    }
    min
}

#[unsafe(no_mangle)]
pub extern "C" fn minf(ptr: *const f64, len: usize) -> f64 {
    if len == 0 {
        return 0.;
    }

    let xs = unsafe { std::slice::from_raw_parts(ptr, len) };

    let mut min = xs[0];
    for &x in xs {
        if x < min {
            min = x;
        }
    }
    min
}

#[unsafe(no_mangle)]
pub extern "C" fn maxi(ptr: *const i64, len: usize) -> i64 {
    if len == 0 {
        return 0;
    }

    let xs = unsafe { std::slice::from_raw_parts(ptr, len) };

    let mut max = xs[0];
    for &x in xs {
        if x > max {
            max = x;
        }
    }
    max
}

#[unsafe(no_mangle)]
pub extern "C" fn maxf(ptr: *const f64, len: usize) -> f64 {
    if len == 0 {
        return 0.;
    }

    let xs = unsafe { std::slice::from_raw_parts(ptr, len) };

    let mut max = xs[0];
    for &x in xs {
        if x > max {
            max = x;
        }
    }
    max
}

#[unsafe(no_mangle)]
pub extern "C" fn clampi(x: i64, min: i64, max: i64) -> i64 {
    if x < min {
        min
    } else if x > max {
        max
    } else {
        x
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn clampf(x: f64, min: f64, max: f64) -> f64 {
    if x < min {
        min
    } else if x > max {
        max
    } else {
        x
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn signi(x: i64) -> i64 {
    if x < 0 {
        -1
    } else if x > 0 {
        1
    } else {
        0
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn signf(x: f64) -> f64 {
    if x < 0. {
        -1.
    } else if x > 0. {
        1.
    } else {
        0.
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn absi(x: i64) -> i64 {
    if x < 0 { -x } else { x }
}

#[unsafe(no_mangle)]
pub extern "C" fn absf(x: f64) -> f64 {
    if x < 0. { -x } else { x }
}

#[unsafe(no_mangle)]
pub extern "C" fn floori(x: i64, d: i64) -> i64 {
    fn inner_floor(x: i64) -> i64 {
        return x - (x % 1);
    }

    if d != 0 {
        inner_floor(x / d) * d
    } else {
        inner_floor(x)
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn floorf(x: f64, d: i64) -> f64 {
    fn inner_floor(x: f64) -> f64 {
        return x - (x % 1.);
    }

    if d != 0 {
        let df = d as f64;
        inner_floor(x / df) * df
    } else {
        inner_floor(x)
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn round(x: f64, d: i64) -> f64 {
    floorf(x * (d as f64) + 0.5, 0)
}

#[unsafe(no_mangle)]
pub extern "C" fn ceil(x: f64, d: i64) -> f64 {
    floorf(x * (d as f64) + 1., 0)
}

#[unsafe(no_mangle)]
pub extern "C" fn powi(x: i64, exp: i64) -> i64 {
    (x as f64).powf(exp as f64) as i64
}

#[unsafe(no_mangle)]
pub extern "C" fn powf(x: f64, exp: f64) -> f64 {
    x.powf(exp)
}

#[warn(unused_variables)]
#[unsafe(no_mangle)]
pub extern "C" fn sqrt(x: f64, term: i64) -> f64 {
    x.sqrt()
}

#[unsafe(no_mangle)]
pub extern "C" fn sin(x: f64, term: i64) -> f64 {
    let mut res = 0f64;
    let term = if term > 10 { 10 } else { term };
    for n in 0..term {
        let en = if n % 2 == 0 { 1.0 } else { -1.0 };
        let de = factorf(2 * n + 1);
        res += (en / de) * x.powf((2 * n + 1) as f64);
    }
    res
}

#[unsafe(no_mangle)]
pub extern "C" fn cos(x: f64, term: i64) -> f64 {
    let mut res = 0f64;
    let term = if term > 10 { 10 } else { term };
    for n in 0..term {
        let en = if n % 2 == 0 { 1.0 } else { -1.0 };
        let de = factorf(2 * n);
        res += (en / de) * x.powf((2 * n) as f64);
    }
    res
}

#[unsafe(no_mangle)]
pub extern "C" fn tan(x: f64, term: i64) -> f64 {
    let s = sin(x, term);
    let c = cos(x, term);

    if approximately(c, 0.0, eps()) {
        if s >= 0.0 {
            f64::INFINITY
        } else {
            f64::NEG_INFINITY
        }
    } else {
        s / c
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn asin(x: f64, term: i64) -> f64 {
    if x.abs() > 1.0 {
        return f64::NAN;
    }

    let mut res = 0.0;
    let mut coef = 1.0;

    let stop = term.abs();

    for n in 0..stop {
        let p = (2 * n + 1) as f64;

        res += coef * (x.powf(p) / p);
        coef *= (2 * n + 1) as f64 / (2 * n + 2) as f64;

        if n > 100000 {
            break;
        }
    }
    res
}

#[unsafe(no_mangle)]
pub extern "C" fn acos(x: f64, term: i64) -> f64 {
    pi() / 2. - asin(x, term)
}

#[unsafe(no_mangle)]
pub extern "C" fn atan(x: f64, term: i64) -> f64 {
    asin(x / sqrt(1. + x.powf(2.), term), term)
}

#[unsafe(no_mangle)]
pub extern "C" fn atan2(y: f64, x: f64, term: i64) -> f64 {
    if x > 0. {
        atan(y / x, term)
    } else if x < 0. && y >= 0. {
        atan(y / x, term) + pi()
    } else if x < 0. && y < 0. {
        atan(y / x, term) - pi()
    } else if approximately(x, 0., eps()) && y > 0. {
        pi() / 2.
    } else if approximately(x, 0., eps()) && y < 0. {
        -pi() / 2.
    } else {
        0.
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn is_prime(n: i64) -> bool {
    if n == 2 {
        true
    } else if n < 2 || n & 2 == 0 {
        false
    } else {
        let stop = floorf(sqrt(n as f64, 20), 0) as i64;
        for i in (3..stop + 1).step_by(2) {
            if n % i == 0 {
                return false;
            }
        }
        true
    }
}

#[unsafe(no_mangle)]
pub extern "C" fn fibonacci(n: i64) -> i64 {
    ((golden_ratio().powf(n as f64) - -golden_ratio().powf(-n as f64)) / sqrt(5., 10)) as i64
}
