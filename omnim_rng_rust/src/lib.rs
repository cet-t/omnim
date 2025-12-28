use pyo3::prelude::*;

#[pyclass]
struct Xorshift64 {
    state: u64,
}

#[pymethods]
impl Xorshift64 {
    #[new]
    fn new(seed: u64) -> Self {
        Xorshift64 {
            state: if seed == 0 { 0xDEADBEEF } else { seed },
        }
    }

    fn next_int(&mut self) -> u64 {
        self.state ^= self.state << 13;
        self.state ^= self.state >> 7;
        self.state ^= self.state << 17;
        self.state
    }

    fn next_float(&mut self) -> f64 {
        let val = self.next_int();
        val as f64 / u64::MAX as f64
    }

    fn next_ints(&mut self, count: usize) -> Vec<u64> {
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            results.push(self.next_int());
        }
        results
    }

    fn next_floats(&mut self, count: usize) -> Vec<f64> {
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            results.push(self.next_float());
        }
        results
    }

    fn random_int(&mut self, min: i64, max: i64) -> i64 {
        let range = (max - min + 1) as u64;
        let val = self.next_int();
        (val % range) as i64 + min
    }

    fn random_float(&mut self, min: f64, max: f64) -> f64 {
        let diff = max - min;
        let val = self.next_float();
        val * diff + min
    }

    fn random_ints(&mut self, count: usize, min: i64, max: i64) -> Vec<i64> {
        let range = (max - min + 1) as u64;
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            let val = self.next_int();
            results.push((val % range) as i64 + min);
        }
        results
    }

    fn random_floats(&mut self, count: usize, min: f64, max: f64) -> Vec<f64> {
        let diff = max - min;
        let inv_max = 1.0 / u32::MAX as f64;
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            let val = self.next_int() as f64;
            results.push((val * inv_max) * diff + min);
        }
        results
    }
}

#[pyclass]
struct Pcg32 {
    state: u64,
    inc: u64,
}

#[pymethods]
impl Pcg32 {
    #[new]
    fn new(seed: u64) -> Self {
        Pcg32 {
            state: seed.wrapping_add(0xDA3E39CB94B95BDB),
            inc: seed | 1,
        }
    }

    fn next_int(&mut self) -> u32 {
        let oldstate = self.state;
        self.state = oldstate
            .wrapping_mul(6364136223846793005)
            .wrapping_add(self.inc);

        let xorshifted = (((oldstate >> 18) ^ oldstate) >> 27) as u32;
        let rot = (oldstate >> 59) as u32;
        (xorshifted >> rot) | (xorshifted << (rot.wrapping_neg() & 31))
    }

    fn next_float(&mut self) -> f64 {
        let val = self.next_int() as f64;
        val / u32::MAX as f64
    }

    fn next_ints(&mut self, count: usize) -> Vec<u32> {
        let mut results = Vec::with_capacity(count);
        for _ in 0..count {
            let oldstate = self.state;
            self.state = oldstate
                .wrapping_mul(6364136223846793005)
                .wrapping_add(self.inc);

            let xorshifted = (((oldstate >> 18) ^ oldstate) >> 27) as u32;
            let rot = (oldstate >> 59) as u32;
            results.push((xorshifted >> rot) | (xorshifted << (rot.wrapping_neg() & 31)));
        }
        results
    }

    fn next_floats(&mut self, count: usize) -> Vec<f64> {
        let mut results = Vec::with_capacity(count);
        for _ in 0..count {
            let val = self.next_int() as f64;
            results.push(val / u32::MAX as f64);
        }
        results
    }

    fn random_int(&mut self, min: i64, max: i64) -> i64 {
        let range = (max - min + 1) as u32;
        let val = self.next_int();
        (val % range) as i64 + min
    }

    fn random_float(&mut self, min: f64, max: f64) -> f64 {
        let diff = max - min;
        let max_val = u32::MAX as f64;
        let val = self.next_int() as f64;
        (val / max_val) * diff + min
    }

    fn random_ints(&mut self, count: usize, min: i64, max: i64) -> Vec<i64> {
        let range = (max - min + 1) as u64;
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            let val = self.next_int() as u64;
            results.push((val % range) as i64 + min);
        }
        results
    }

    fn random_floats(&mut self, count: usize, min: f64, max: f64) -> Vec<f64> {
        let diff = max - min;
        let inv_max = 1.0 / u32::MAX as f64;
        let mut results = Vec::with_capacity(count);

        for _ in 0..count {
            let val = self.next_int() as f64;
            results.push((val * inv_max) * diff + min);
        }
        results
    }
}

#[pyclass]
struct BinarySearch {
    generator: Pcg32,
}

#[pymethods]
impl BinarySearch {
    #[new]
    fn new(seed: u64) -> Self {
        BinarySearch {
            generator: Pcg32::new(seed),
        }
    }

    fn search(&mut self, weights: Vec<f64>) -> i64 {
        let length = weights.len();
        if length < 1 {
            return -1;
        }

        let mut total_weights = 0f64;
        let mut accumulate_weights = Vec::with_capacity(length);

        for weight in weights {
            total_weights += weight;
            accumulate_weights.push(total_weights);
        }

        let r = self.generator.random_float(0., total_weights);
        let mut bottom = 0;
        let mut top = length as i64 - 1;

        while bottom < top {
            let middle = (bottom + top) / 2;
            if r > accumulate_weights[middle as usize] {
                bottom = middle + 1;
            } else {
                let p = if middle > 0 {
                    accumulate_weights[middle as usize - 1]
                } else {
                    0.0
                };
                if r >= p {
                    return middle;
                }
                top = middle;
            }
        }
        return top;
    }
}

#[pymodule]
fn omnim_rng_rust(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Xorshift64>()?;
    m.add_class::<Pcg32>()?;
    m.add_class::<BinarySearch>()?;
    Ok(())
}
