use pyo3::prelude::*;

#[pyfunction]
fn search(_query: String) -> PyResult<Vec<String>> {
    Ok(vec![])
}

#[pymodule]
fn rust_searcher(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(search, m)?)?;
    Ok(())
}
