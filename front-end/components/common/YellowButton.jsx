import React from 'react'
import styled from 'styled-components';
import { lighten, darken } from 'polished';

function YellowButton({ children, paddingTop, paddingRight, type, onClick }) {
  return (
    <StyledYellowButton type={type} paddingTop={paddingTop} paddingRight={paddingRight} onClick={onClick}>
      {children}
    </StyledYellowButton>
  )
}
export default YellowButton;

const StyledYellowButton = styled.button`
  padding: ${({ paddingTop }) => paddingTop} ${({ paddingRight }) => paddingRight};
  border-radius: 1.5625rem;
  

  background-color: #FFD358;
  color: #343434;
  font-family: 'Pretendard-SemiBold';
  font-size: 1rem;

  box-shadow: 0.2rem 0.2rem 0.5rem 0.2rem rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: 300ms;
  &:hover {
    background-color: ${lighten(0.02, '#FFD358')};
    box-shadow: 0.2rem 0.2rem 0.5rem 0.2rem rgba(0, 0, 0, 0.15);
  }
  &:active {
    background-color: ${darken(0.02, '#FFD358')};
`;
