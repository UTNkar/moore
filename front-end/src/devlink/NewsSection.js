import React from 'react';

import * as _Builtin from './_Builtin';
import * as _interactions from './interactions';

const _interactionsData = JSON.parse(
  '{"events":{"e-22":{"id":"e-22","name":"","animationType":"custom","eventTypeId":"MOUSE_OVER","action":{"id":"","actionTypeId":"GENERAL_START_ACTION","config":{"delay":0,"easing":"","duration":0,"actionListId":"a-12","affectedElements":{},"playInReverse":false,"autoStopEventId":"e-23"}},"mediaQueries":["main","medium","small","tiny"],"target":{"id":"6564d41f856f099dcc4e8a45|6fe8fb93-163c-f108-6420-ff65e648aa74","appliesTo":"ELEMENT","styleBlockIds":[]},"targets":[{"id":"6564d41f856f099dcc4e8a45|6fe8fb93-163c-f108-6420-ff65e648aa74","appliesTo":"ELEMENT","styleBlockIds":[]}],"config":{"loop":false,"playInReverse":false,"scrollOffsetValue":null,"scrollOffsetUnit":null,"delay":null,"direction":null,"effectIn":null},"createdOn":1705048602048},"e-23":{"id":"e-23","name":"","animationType":"custom","eventTypeId":"MOUSE_OUT","action":{"id":"","actionTypeId":"GENERAL_START_ACTION","config":{"delay":0,"easing":"","duration":0,"actionListId":"a-13","affectedElements":{},"playInReverse":false,"autoStopEventId":"e-22"}},"mediaQueries":["main","medium","small","tiny"],"target":{"id":"6564d41f856f099dcc4e8a45|6fe8fb93-163c-f108-6420-ff65e648aa74","appliesTo":"ELEMENT","styleBlockIds":[]},"targets":[{"id":"6564d41f856f099dcc4e8a45|6fe8fb93-163c-f108-6420-ff65e648aa74","appliesTo":"ELEMENT","styleBlockIds":[]}],"config":{"loop":false,"playInReverse":false,"scrollOffsetValue":null,"scrollOffsetUnit":null,"delay":null,"direction":null,"effectIn":null},"createdOn":1705048602049},"e-24":{"id":"e-24","name":"","animationType":"custom","eventTypeId":"MOUSE_OVER","action":{"id":"","actionTypeId":"GENERAL_START_ACTION","config":{"delay":0,"easing":"","duration":0,"actionListId":"a-12","affectedElements":{},"playInReverse":false,"autoStopEventId":"e-25"}},"mediaQueries":["main","medium","small","tiny"],"target":{"id":"5e557930-8cad-cab8-74b9-5272409c361f","appliesTo":"ELEMENT","styleBlockIds":[]},"targets":[{"id":"5e557930-8cad-cab8-74b9-5272409c361f","appliesTo":"ELEMENT","styleBlockIds":[]}],"config":{"loop":false,"playInReverse":false,"scrollOffsetValue":null,"scrollOffsetUnit":null,"delay":null,"direction":null,"effectIn":null},"createdOn":1705049438828},"e-25":{"id":"e-25","name":"","animationType":"custom","eventTypeId":"MOUSE_OUT","action":{"id":"","actionTypeId":"GENERAL_START_ACTION","config":{"delay":0,"easing":"","duration":0,"actionListId":"a-13","affectedElements":{},"playInReverse":false,"autoStopEventId":"e-24"}},"mediaQueries":["main","medium","small","tiny"],"target":{"id":"5e557930-8cad-cab8-74b9-5272409c361f","appliesTo":"ELEMENT","styleBlockIds":[]},"targets":[{"id":"5e557930-8cad-cab8-74b9-5272409c361f","appliesTo":"ELEMENT","styleBlockIds":[]}],"config":{"loop":false,"playInReverse":false,"scrollOffsetValue":null,"scrollOffsetUnit":null,"delay":null,"direction":null,"effectIn":null},"createdOn":1705049438829}},"actionLists":{"a-12":{"id":"a-12","title":"News List Item (enter)","actionItemGroups":[{"actionItems":[{"id":"a-12-n","actionTypeId":"STYLE_TEXT_COLOR","config":{"delay":0,"easing":"outQuint","duration":350,"target":{"useEventTarget":"CHILDREN","selector":".news-list-item-title","selectorGuids":["2a0aca36-e4c7-8f26-a5f6-1d2dd2c662d5"]},"globalSwatchId":"","rValue":0,"bValue":152,"gValue":76,"aValue":1}},{"id":"a-12-n-3","actionTypeId":"TRANSFORM_SCALE","config":{"delay":0,"easing":"outQuint","duration":350,"target":{"useEventTarget":"CHILDREN","selector":".news-list-item-thumbnail-wrapper","selectorGuids":["babc3d5d-9d47-b2d8-5fa3-ffc6fcac47b9"]},"xValue":0.9,"yValue":0.9,"locked":true}}]}],"useFirstGroupAsInitialState":false,"createdOn":1705048619020},"a-13":{"id":"a-13","title":"News List Item (leave)","actionItemGroups":[{"actionItems":[{"id":"a-13-n","actionTypeId":"STYLE_TEXT_COLOR","config":{"delay":0,"easing":"outQuint","duration":350,"target":{"useEventTarget":"CHILDREN","selector":".news-list-item-title","selectorGuids":["2a0aca36-e4c7-8f26-a5f6-1d2dd2c662d5"]},"globalSwatchId":"","rValue":33,"bValue":39,"gValue":36,"aValue":1}},{"id":"a-13-n-3","actionTypeId":"TRANSFORM_SCALE","config":{"delay":0,"easing":"outQuint","duration":350,"target":{"useEventTarget":"CHILDREN","selector":".news-list-item-thumbnail-wrapper","selectorGuids":["babc3d5d-9d47-b2d8-5fa3-ffc6fcac47b9"]},"xValue":1,"yValue":1,"locked":true}}]}],"useFirstGroupAsInitialState":false,"createdOn":1705048757898}},"site":{"mediaQueries":[{"key":"main","min":992,"max":10000},{"key":"medium","min":768,"max":991},{"key":"small","min":480,"max":767},{"key":"tiny","min":0,"max":479}]}}',
);

export function NewsSection({ as: _Component = _Builtin.Section }) {
  _interactions.useInteractions(_interactionsData);

  return (
    <_Component
      className="section"
      grid={{
        type: 'section',
      }}
      tag="section"
    >
      <_Builtin.VFlex className="container" tag="div">
        <_Builtin.Heading tag="h2">{'Nyheter'}</_Builtin.Heading>
        <_Builtin.NotSupported _atom="DynamoWrapper" />
      </_Builtin.VFlex>
    </_Component>
  );
}
