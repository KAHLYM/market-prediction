import { Pipe, PipeTransform } from '@angular/core';

@Pipe({
  name: 'absolute'
})
export class AbsolutePipe implements PipeTransform {

  transform(value: string, ...args: unknown[]): string {

    return String(Math.abs(Number(value)));
  }

}
