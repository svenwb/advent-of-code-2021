use std::fs::File;
use std::io::{BufRead, BufReader};

pub fn solve_sonar_sweep(sonar_seep_report: &[usize]) -> usize {
    let pairs = (0..sonar_seep_report.len()-1).zip(1..sonar_seep_report.len()).collect::<Vec<(usize, usize)>>();
    let mut increase_counter = 0;
    for (previous, current) in pairs {
        if sonar_seep_report[previous] < sonar_seep_report[current] {
            increase_counter += 1;
        }
    }
    increase_counter
}

pub fn solve_sonar_sweep_sliding_window(sonar_seep_report: &[usize]) -> usize {
    let mut increase_counter = 0;
    for i in 0..sonar_seep_report.len()-2 {
        let window_a : usize = sonar_seep_report[i..i+2].iter().sum();
        let window_b = sonar_seep_report[i+1..i+3].iter().sum();
        if window_a < window_b {
            increase_counter += 1;
        }
    }
    increase_counter
}

pub fn read_sonar_report_from_file(path: &str) -> Vec<usize>{
    let file = File::open(path).unwrap();
    let reader = BufReader::new(file);

    reader.lines().map(|line| line.unwrap().parse::<usize>().unwrap()).collect()
}

#[cfg(test)]
mod test {
    use crate::day1::{read_sonar_report_from_file, solve_sonar_sweep, solve_sonar_sweep_sliding_window};

    #[test]
    fn test_read_file() {
        let data = read_sonar_report_from_file("/Users/I526463/repos/advent-of-code-2021/input/day1");
        assert_eq!(data[0], 104);
        assert_eq!(data.len(), 2000);
    }

    #[test]
    fn test_solve_sonar_sweep() {
        let counter = solve_sonar_sweep(&[1,2,0]);
        assert_eq!(counter, 1)
    }

    #[test]
    fn solution_1() {
        let data = read_sonar_report_from_file("/Users/I526463/repos/advent-of-code-2021/input/day1");
        let counter = solve_sonar_sweep(&data);
        assert_eq!(counter, 1527)
    }

    #[test]
    fn test_solve_sonar_sweep_sliding_window() {
        let counter = solve_sonar_sweep_sliding_window(&[1,2,3,2,1,9]);
        assert_eq!(counter, 2)
    }

    #[test]
    fn solution_2() {
        let data = read_sonar_report_from_file("/Users/I526463/repos/advent-of-code-2021/input/day1");
        let counter = solve_sonar_sweep_sliding_window(&data);
        assert_eq!(counter, 1502)
    }
}