import { TrailingZeroPipe } from './trailing-zero.pipe';

describe('TrailingZeroPipe', () => {
  it('create an instance', () => {
    const pipe = new TrailingZeroPipe();
    expect(pipe).toBeTruthy();
  });

  it('adds trailing zeros to no decimal place', () => {
    const pipe = new TrailingZeroPipe();
    expect(pipe.transform("1")).toBe("1.00");
  });

  it('adds trailing zeros to one decimal place', () => {
    const pipe = new TrailingZeroPipe();
    expect(pipe.transform("1.2")).toBe("1.20");
  });

  it('does not add trailing zeros to two decimal places', () => {
    const pipe = new TrailingZeroPipe();
    expect(pipe.transform("1.23")).toBe("1.23");
  });
});