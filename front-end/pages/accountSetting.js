import React, { useEffect, useState } from "react";
import NavBar from "../components/NavBar";
import styled from "styled-components";
import { useDispatch, useSelector } from "react-redux";
import Layout from "../hocs/Layout";
import { load_user, check_auth_status } from "../redux/actions/auth";
import { useRouter } from "next/router";
import ProfileInfoBox from "../components/accountSetting/ProfileInfoBox";
import FlexRow from "../components/common/FlexRow";
import WhiteButton from "../components/common/WhiteButton";
import GreyInput from "../components/common/GreyInput";
import YellowButton from "../components/common/YellowButton";
import YellowTitle from "../components/common/YellowTitle";
import ContentText from "../components/common/ContentText";
import FlexColumn from "../components/common/FlexColumn";
import { PageTitle } from "../pages/findPassword";
import BioUpdateBox from "../components/accountSetting/BioUpdateBox";
import NicknameUpdateBox from "../components/accountSetting/NicknameUpdateBox";
import PasswordSetBox from "../components/accountSetting/PasswordSetBox";
import { Alert } from "../components/Alert";

function accountSetting() {
  //1. profileImg변경하기 O
  //2. profileBio변경하기
  //3. email주소 보여주기
  //4. 닉네임 변경하기
  //5. 비밀번호 변경하기
  //5-1.기존 비밀번호 맞는지 확인하기
  //5-2 맞으면 입력된 값으로 수정하기
  const router = useRouter();
  const dispatch = useDispatch();
  //0. user정보 받아오기
  const user = useSelector((state) => state.auth.user);
  const [token, setToken] = useState("");

  const getAccessToken = async () => {
    if (dispatch && dispatch !== null && dispatch !== undefined) {
      dispatch(check_auth_status())
        .then((res) => res.json())
        .then((data) => {
          const accessToken = data.access;
          setToken(accessToken);
        })
        .catch((err) => console.log(err));
    }
  };

  const onClickLogout = async (e) => {
    e.preventDefault();
    await dispatch(logout());
    router.push("/");
  };

  //token 확인(refresh, verify)
  useEffect(() => {
    if (dispatch && dispatch !== null && dispatch !== undefined)
      dispatch(check_auth_status());
    getAccessToken();
  }, [dispatch]);

  return (
    <>
      <Layout
        title="Diggging | 계정설정"
        content="개발자들을 위한 커뮤니티 디깅 계정설정 페이지"
      >
        <NavBar />
        {user?.user.id ? (
          <>
            <Alert />
            <FormBox>
              <PageTitle>계정 설정하기</PageTitle>
              <NicknameBox>
                <ProfileTitle>{user.user.user_nickname}</ProfileTitle>
                <ProfileTitle2>님의 프로필</ProfileTitle2>
              </NicknameBox>
              <ProfileInfoBox userData={user} token={token} />
              <BioUpdateBox userData={user} token={token} />
              <ProfileBox padding="2.375rem">
                <YellowTitle>이메일</YellowTitle>
                {/* <ContentText>{email}</ContentText> */}
              </ProfileBox>
              <NicknameUpdateBox userData={user} token={token} />
              <PasswordSetBox userData={user} token={token} />
              <AccountBtnBox>
                {/* <WhiteButton paddingTop="0.625rem" paddingRight="2rem" fontSize="0.8125rem">회원탈퇴 😥</WhiteButton> */}
                <WhiteButton
                  onSubmit={(e) => onClickLogout(e)}
                  type="submit"
                  paddingTop="0.625rem"
                  paddingRight="2rem"
                  fontSize="0.8125rem"
                >
                  로그아웃 💨{" "}
                </WhiteButton>
              </AccountBtnBox>
              {/* <Link href="">변경하기</Link> 여기에 reset password url필요 */}
            </FormBox>
          </>
        ) : null}
      </Layout>
    </>
  );
}

export { ProfileBioBox, ProfileBox };
export default accountSetting;

const FormBox = styled.div`
  width: 49.375rem;
  margin: auto auto;
  margin-top: 11.25rem;
  position: relative;
`;

const NicknameBox = styled.header`
  margin-top: 5.375rem;
  margin-bottom: 1.875rem;
  padding-bottom: 1.5rem;
  border-bottom: solid 1px #e5e5e5;
`;

const ProfileTitle = styled.span`
  font-size: 1.625rem;
  color: #ffba42;
  font-family: "Pretendard-Bold";
  margin-bottom: 1.5rem;
`;

const ProfileTitle2 = styled.span`
  font-size: 1.25rem;
  color: #ffba42;
  font-family: "Pretendard-Bold";
  margin-left: 0.125rem;
`;

const ProfileBox = styled.form`
  display: flex;
  flex-direction: row;
  padding: ${({ padding }) => padding} 0;
  border-bottom: solid 2px #e5e5e5;
  justify-content: flex-start;
  align-items: baseline;
  justify-content: space-between;
  position: relative;
`;

const ProfileBioBox = styled(ProfileBox)`
  justify-content: flex-start;
  position: relative;
`;

const AccountBtnBox = styled.form`
  display: flex;
  margin-top: 4rem;
  flex-direction: row;
  justify-content: flex-end;
`;
