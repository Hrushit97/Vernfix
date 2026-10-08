import { v4 as uuidv4 } from 'uuid';

export class Passenger {
  constructor(firstName, lastName, email, phone) {
    this.id = uuidv4();
    this.firstName = firstName;
    this.lastName = lastName;
    this.email = email;
    this.phone = phone;
    this.passportNumber = null;
  }

  getFullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  setPassportNumber(passportNumber) {
    this.passportNumber = passportNumber;
  }

  getPassengerInfo() {
    return {
      id: this.id,
      name: this.getFullName(),
      email: this.email,
      phone: this.phone,
      passport: this.passportNumber || 'Not provided'
    };
  }
}
