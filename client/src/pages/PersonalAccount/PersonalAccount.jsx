import React from "react";
import { AverageButton } from "../../shared/Buttons/AverageButton/AverageButton";
import { Link } from "react-router-dom";
export function PersonalAccount() {
  return <div><div style={{ 
  display: 'inline-flex', 
  gap: '10px',
  flexWrap: 'wrap' /* если не помещается - перенос на новую строку */
}}>
  <Link to={`/`}>
    <AverageButton>кнопка назад</AverageButton>
  </Link>

</div></div>;
}
