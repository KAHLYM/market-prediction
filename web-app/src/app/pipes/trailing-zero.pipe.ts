import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'trailingZero'
})
export class TrailingZeroPipe implements PipeTransform {

  transform(value: string, ...args: unknown[]): string {
    let charactersAfterDecimalPlace: number = value.indexOf(".") == -1 ? 0 : value.length - value.indexOf(".") - 1;
    if (!charactersAfterDecimalPlace) {
      value += ".";
    }
    value += "0".repeat(2 - charactersAfterDecimalPlace);
    return value;
  }

}
