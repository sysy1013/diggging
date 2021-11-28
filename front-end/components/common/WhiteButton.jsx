import React from 'react'
import styled from 'styled-components';

function WhiteButton({ paddingTop, paddingRight, fontSize, children }) {
  return (
    <StyledButton
      paddingTop={paddingTop}
      paddingRight={paddingRight}
      fontSize={fontSize}
    >{children}</StyledButton>
  )
}

export default WhiteButton;
//0.625rem 1.5625rem;
const StyledButton = styled.button`
  padding-top: ${({ paddingTop }) => paddingTop};
  padding-bottom: ${({ paddingTop }) => paddingTop};
  padding-right: ${({ paddingRight }) => paddingRight};
  padding-left: ${({ paddingRight }) => paddingRight};

  border-radius: 1.25rem;
  border: solid 3px white;
  cursor: pointer;

  background-color: #FBFBFB;
  opacity: 80%;

  color: #5F5F5F;
  font-family: 'Pretendard-SemiBold';
  font-size: ${({ fontSize }) => fontSize};
  box-shadow: 0 0.25rem 0.75rem 0 rgba(0, 0, 0, 0.1);
`;
