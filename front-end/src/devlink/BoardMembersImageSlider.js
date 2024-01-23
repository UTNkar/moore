import React from 'react';

import * as _Builtin from './_Builtin';

export function BoardMembersImageSlider({ as: _Component = _Builtin.SliderWrapper }) {
  return (
    <_Component
      className="large-image-slider"
      navSpacing={4}
      navShadow={false}
      autoplay={true}
      delay={2000}
      iconArrows={true}
      animation="slide"
      navNumbers={false}
      easing="ease-out-quint"
      navRound={true}
      hideArrows={false}
      disableSwipe={false}
      duration={350}
      infinite={true}
      autoMax={0}
      navInvert={false}
    >
      <_Builtin.SliderMask className="large-image-wrapper">
        <_Builtin.SliderSlide className="large-image-slider-item" tag="div">
          <_Builtin.Image
            className="large-image tall"
            loading="lazy"
            height="auto"
            width="auto"
            aria-describedby="image-desc"
            alt="Uppsala teknolog- och naturvetarkårs styrelse"
            src="https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/656e11cffb36ecc1b04c9795_styrelsen.jpeg"
          />
        </_Builtin.SliderSlide>
        <_Builtin.SliderSlide className="large-image-slider-item" tag="div">
          <_Builtin.Image
            className="large-image tall"
            loading="lazy"
            height="auto"
            width="auto"
            aria-describedby="image-desc"
            alt="Uppsala teknolog- och naturvetarkårs styrelse"
            src="https://uploads-ssl.webflow.com/655e29844518537470ba5b0f/656e1d11828cbcf14672b950_styrelsen-fun.jpeg"
          />
        </_Builtin.SliderSlide>
      </_Builtin.SliderMask>
      <_Builtin.SliderArrow className="slider-horizontal-navigator" dir="left">
        <_Builtin.Block className="icon" tag="div">
          {'arrow_back_ios'}
        </_Builtin.Block>
      </_Builtin.SliderArrow>
      <_Builtin.SliderArrow className="slider-horizontal-navigator" dir="right">
        <_Builtin.Block className="icon" tag="div">
          {'arrow_forward_ios'}
        </_Builtin.Block>
      </_Builtin.SliderArrow>
      <_Builtin.SliderNav />
    </_Component>
  );
}
