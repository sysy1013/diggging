import React, {useState} from 'react'
import axios from 'axios';
import {API_URL} from '../config/index'
import Layout from '../hocs/Layout';
import styled from 'styled-components';
import NavBar from '../components/NavBar';
import GreyInput from '../components/common/GreyInput';
import YellowButton from "../components/common/YellowButton";
import YellowTitle from '../components/common/YellowTitle';


function findPassword() {
  const [email, setEmail] = useState('');
  const [message, setMessage] = useState('');
  const onInput = (e) => {
    setEmail(e.target.value);
  }

  //API주소 과연맞는가... 404에러뜬다
  const findPassword = async (e, email) => {
    e.preventDefault();
    await axios.post(`${API_URL}/users/api/password_reset_done`, {
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'text/plain',
        // 'Access-Control-Allow-Origin': '*', //cors에러때문에 넣어본 것들...
        // 'Access-Control-Allow-Methods': 'POST',
        // 'Access-Control-Max-Age': 3600,
        // 'Access-Control-Allow-Headers': origin,
      },
      credentials: "include",
      email: email
    })
    .then(response => {
      setMessage("입력하신 이메일주소로 비밀번호 변경 링크를 보내드렸습니다.")
    })
    .catch(error => setMessage(`${error} 이메일 발송중 오류가 발생했습니다.`))
  }
  return (
    <>
      <Layout/>
      <NavBar />
      <FormBox>
        <PageTitle>비밀번호 찾기</PageTitle>
        <GuideMessage>가입하신 이메일을 입력하시면 해당 주소로 비밀번호 변경 링크를 보내드립니다.</GuideMessage>
        <form onSubmit={findPassword} type="POST">
          <YellowTitle fontSize="1.375rem" >이메일</YellowTitle>
          <GreyInput
            width="28.75rem"
            height="3.125rem"
            marginRight="2.875rem"
            marginLeft="2.75rem"
            type="email"
            name="email"
            placeholder="이메일"
            onChange={onInput}
            value={email}
            required
          />
          <YellowButton paddingTop="0.9375rem" paddingRight="2.1875rem" >전송</YellowButton>
        </form>
      </FormBox>
    </>
  )
}

const FormBox = styled.section`
  width: 49.375rem;
  margin: auto auto;
  margin-top: 11.25rem;
`;

const PageTitle = styled.span`
  font-family: 'Pretendard-Bold';
  font-size: 1.625rem;
  color: #343434;
  padding-bottom: 0.375rem;
  border-bottom: solid 3px #343434;
`;

const GuideMessage = styled.p`
  display: block;
  color: #8D8C85;
  font-size: 1.125rem;
  font-family: "Pretendard-Medium";
  border-top: solid 2px #E5E5E5;
  margin-top: 95px;
  padding-top: 20px;
  margin-bottom: 40px;
`;

export {FormBox, PageTitle, GuideMessage};
export default findPassword;
