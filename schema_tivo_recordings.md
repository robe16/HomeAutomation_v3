# Schema for data returned when retrieving recorded shows from TiVo devices


<?xml version="1.0" encoding="utf-8"?>
<TiVoContainer xmlns="http://www.tivo.com/developer/calypso-protocol-1.6/">
  <Details>
      <ContentType>x-tivo-container/tivo-videos</ContentType>
      <SourceFormat>x-tivo-container/tivo-dvr</SourceFormat>
      <Title>Now Playing</Title>
      <LastChangeDate>0x577D7A25</LastChangeDate>
      <TotalItems>18</TotalItems>
      <UniqueId>/NowPlaying</UniqueId>
  </Details>
  <SortOrder>Type,CaptureDate</SortOrder>
  <GlobalSort>Yes</GlobalSort>
  <ItemStart>0</ItemStart>
  <ItemCount>16</ItemCount>
  <Item>
      <Details>
          <ContentType>video/x-tivo-raw-tts</ContentType>
          <SourceFormat>video/x-tivo-raw-tts</SourceFormat>
          <Title>24 Hours in A&amp;E</Title>
          <CopyProtected>Yes</CopyProtected>
          <SourceSize>4729077760</SourceSize>
          <Duration>3899000</Duration>
          <CaptureDate>0x577D6302</CaptureDate>
          <ShowingDuration>3600000</ShowingDuration>
          <StartPadding>60000</StartPadding>
          <EndPadding>240000</EndPadding>
          <ShowingStartTime>0x577D6340</ShowingStartTime>
          <Description>Cyclist Athar, who's 22, is rushed to St George's...</Description>
          <SourceChannel>142</SourceChannel>
          <SourceStation>4 HD</SourceStation>
          <HighDefinition>Yes</HighDefinition>
          <ProgramId>EP014129450131</ProgramId>
          <SeriesId>SH01412945</SeriesId>
          <StreamingPermission>Yes</StreamingPermission>
          <ShowingBits>20996</ShowingBits>
          <SourceType>2</SourceType>
          <IdGuideSource>50716</IdGuideSource>
      </Details>
      <Links>
          <Content>
              <Url>http://192.168.0.111:80/download/24%20Hours%20in%20A%26E.TiVo?Container=%2FNowPlaying&amp;id=1360</Url>
              <ContentType>video/x-tivo-raw-tts</ContentType>
              <Available>No</Available>
          </Content><CustomIcon>
          <Url>urn:tivo:image:save-until-i-delete-recording</Url>
          <ContentType>image/*</ContentType>
          <AcceptsParams>No</AcceptsParams>
          </CustomIcon><TiVoVideoDetails>
          <Url>https://192.168.0.111:443/TiVoVideoDetails?id=1360</Url>
          <ContentType>text/xml</ContentType>
          <AcceptsParams>No</AcceptsParams>
          </TiVoVideoDetails>
      </Links>
  </Item>
  <Item>
          etc.
  </Item>
</TiVoContainer>