import { statusToColor } from '@/consts/invoice'

export { statusToColor }

export const sumSubStyles = `
.submit {
  margin-top: 20px
}

.mobile-button {
  box-shadow: none;
  color: blue;
  position: absolute;
  bottom: -25px;
  right: 0;
  background-color: transparent;
  width: 250px;
}

.mobile-button > div > h3 {
  color: #0060FF;
  text-decoration: underline;
  font-size: 11px
}

.mobile-button > .fa-icon {
  fill: #0060FF;
  width: 50px;
  height: 50px;
}

:root {
  --primary-color: black;
}

strong {
  font-weight: normal;
}

.steps {
  display: none;
}

.desktop {
 margin: 0
}

section .row {
  margin: 16px 0
}

.content {
  margin: -35px 0 0 0;
  padding: 0;
}

section {
  box-shadow: none;
}

.row:nth-child(3) > h3 {
  display: none
}

.row:nth-child(2) > h3 {
  font-weight: normal
}

.row > h2 {
  text-align: left;
}

.row > h2 > p {
  color: #E0B72E;
  text-transform: lowercase;
}

.radio-group {
  width: 1000px
}

.sumsub-logo {
  display: none
}

div > .row:last-child {
  text-align: left
}
`
